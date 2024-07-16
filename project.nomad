# Variables used below and their defaults if not set externally
variables {
  CI_REGISTRY = "registry.sphericalelephant.com"
  CI_REGISTRY_IMAGE = "registry.sphericalelephant.com/parat/parat"
  CI_COMMIT_REF_SLUG = "main"
  CI_COMMIT_SHA = "latest"
  CI_PROJECT_PATH_SLUG = "parat-parat"
  CI_REGISTRY_USER = ""
  CI_REGISTRY_PASSWORD = ""
  # optional but suggested CI/CD group or project vars
  CI_R2_USER = ""
  CI_R2_PASS = ""

  STAGE = "development"

  MEMORY = 256 # MB
  CPU = 256 # MHz

  COUNT = 1

  UMAMI_ID = ""
}

variable "HOSTNAMES" {
  # This autogenerates from .gitlab-ci.yml
  # but you can override to 1 or more custom hostnames if desired, eg:
  #   NOMAD_VAR_HOSTNAMES='["www.example.com", "site.example.com"]'
  type = list(string)
  default = ["group-project-branch-slug.example.com"]
}

locals {
  slug = "parat_${var.STAGE}_parat"
  # service names must be valid RFC1123. so "-" instead of "_"
  slug_dashed = "parat-${var.STAGE}-parat"
  allowed_hosts = format("%#v", var.HOSTNAMES)
  csrf_hosts = format("'%#v'", formatlist("https://%s",var.HOSTNAMES))
}

# NOTE: for main branch: NOMAD_VAR_SLUG === CI_PROJECT_PATH_SLUG
job "NOMAD_VAR_SLUG" {
  datacenters = ["nbg1", "fsn1"]
  namespace = "parat"

  group "parat" {
    count = var.COUNT

    update {
      max_parallel = 1
      min_healthy_time = "30s"
      healthy_deadline = "5m"
      progress_deadline = "10m"
      auto_revert = true
    }
    restart {
      attempts = 3
      delay    = "15s"
      interval = "30m"
      mode     = "fail"
    }

    volume "NOMAD_VAR_SLUG_DASHED" {
      type = "csi"
      read_only = false
      source = "${local.slug_dashed}"
      access_mode = "multi-node-multi-writer"
      attachment_mode = "file-system"
    }

    task "migrate-parat-parat" {
      driver = "docker"

      lifecycle {
        hook = "prestart"
        sidecar = false
      }

      config {
        advertise_ipv6_address = true
        image = "${var.CI_REGISTRY_IMAGE}/parat:${var.CI_COMMIT_SHA}"
        args = ["python", "manage.py", "migrate"]

        auth {
          server_address = "${var.CI_REGISTRY}"
          username = element([for s in [var.CI_R2_USER, var.CI_REGISTRY_USER] : s if s != ""], 0)
          password = element([for s in [var.CI_R2_PASS, var.CI_REGISTRY_PASSWORD] : s if s != ""], 0)
        }

        logging {
          type = "journald"
        }
      }

      template {
        data = <<-EOH
        {{ with secret "kv/data/parat/parat/${var.STAGE}" }}
        DJANGO_DATABASE_URL=postgres://${local.slug}:{{ .Data.data.database_password | toJSON }}@hez-fsn1-pgsql01-a.in.sphericalelephant.cloud/parat?options=--search_path%3d${var.STAGE}-parat
        DJANGO_SECRET_KEY={{ .Data.data.secret_key }}
        DJANGO_WAGTAILTRANSFER_SECRET_KEY={{ .Data.data.wagtail_transfer_key }}
        DJANGO_WAGTAILTRANSFER_STAGE_KEY={{ .Data.data.wagtail_transfer_key }}
        DJANGO_EMAIL_SERVER={{ .Data.data.email_server }}
        {{ end }}
        DJANGO_ENVIRONMENT=${var.STAGE}
        DJANGO_ERROR_EMAILS='["f.shahbazi@sphericalelephant.com", "m.holczmann@sphericalelephant.com"]'
        EOH
        env = true
        destination = ".env"
      }
    }

    task "parat" {
      driver = "docker"

      config {
        advertise_ipv6_address = true
        auth {
          server_address = "${var.CI_REGISTRY}"
          username = element([for s in [var.CI_R2_USER, var.CI_REGISTRY_USER] : s if s != ""], 0)
          password = element([for s in [var.CI_R2_PASS, var.CI_REGISTRY_PASSWORD] : s if s != ""], 0)
        }
        image = "${var.CI_REGISTRY_IMAGE}/parat:${var.CI_COMMIT_SHA}"
        logging {
          type = "journald"
        }
        # The MEMORY var now becomes a **soft limit**
        # We will 10x that for a **hard limit**
        memory_hard_limit = "${var.MEMORY * 10}"
      }

      resources {
        memory = "${var.MEMORY}"
        cpu = "${var.CPU}"
      }

      template {
        data = <<-EOH
        {{ with secret "kv/data/parat/parat/${var.STAGE}" }}
        DJANGO_DATABASE_URL=postgres://${local.slug}:{{ .Data.data.database_password | toJSON }}@hez-fsn1-pgsql01-a.in.sphericalelephant.cloud/parat?options=--search_path%3d${var.STAGE}-parat
        DJANGO_SECRET_KEY={{ .Data.data.secret_key }}
        DJANGO_EMAIL_SERVER={{ .Data.data.email_server }}
        DJANGO_WAGTAILTRANSFER_SECRET_KEY={{ .Data.data.wagtail_transfer_key }}
        DJANGO_WAGTAILTRANSFER_STAGE_KEY={{ .Data.data.wagtail_transfer_key }}
        DJANGO_FRIENDLY_CAPTCHA_API_KEY={{ .Data.data.friendly_captcha_api_key }}
        {{ end }}
        DJANGO_STAGE=${var.STAGE}
        DJANGO_UMAMI_ID=${var.UMAMI_ID}
        DJANGO_CSRF_HOSTS=${local.csrf_hosts}
        EOH
        env = true
        destination = ".env"
      }

      volume_mount {
        volume = "${local.slug_dashed}"
        destination = "/home/app/parat/media"
        read_only = false
      }

      service {
        name = "${local.slug_dashed}-http"
        tags = [
          "traefik.enable=true",
          format("traefik.http.routers.${local.slug}.rule=Host(%s)", join(", ", formatlist("`%s`", var.HOSTNAMES))),
          "traefik.http.middlewares.${local.slug}-compress.compress=true",
          "traefik.http.routers.${local.slug}.middlewares=${local.slug}-compress"
        ]
        port = 8000
        address_mode = "driver"

        check {
          name = "alive"
          type = "http"
          port = 8000
          path = "/"
          interval = "60s"
          timeout  = "2s"
          address_mode = "driver"
          header {
            Host = ["${var.HOSTNAMES[0]}"]
          }
          check_restart {
            limit = 3
            grace = "20s"
          }
        }
      }
    }

    task "nginx" {
      driver = "docker"

      config {
        advertise_ipv6_address = true
        image = "nginx:alpine"
        logging {
          type = "journald"
        }
      }

      resources {
        memory = 64
        cpu = 128
      }

      volume_mount {
        volume = "${local.slug_dashed}"
        destination = "/usr/share/nginx/html/media"
        read_only = true
      }

      service {
        name = "${local.slug_dashed}-media"
        tags = [
          "traefik.enable=true",
          format("traefik.http.routers.${local.slug}-media.rule=Host(%s) && PathPrefix(`/media`)", join(", ", formatlist("`%s`", var.HOSTNAMES))),
          "traefik.http.middlewares.${local.slug}-media-redirects.redirectregex.regex=^https?:\\/\\/.*\\/(media\\/\\w{2}\\/\\w{2}\\/\\w{2}\\/\\d+\\/.*)$$",
          "traefik.http.middlewares.${local.slug}-media-redirects.redirectregex.replacement=https://products.parat.de/$${1}",
          "traefik.http.routers.${local.slug}-media.middlewares=${local.slug}-media-redirects"
        ]
        port = 80
        address_mode = "driver"

        check {
          name = "alive"
          type = "http"
          port = 80
          path = "/"
          interval = "60s"
          timeout  = "2s"
          address_mode = "driver"
          check_restart {
            limit = 3
            grace = "20s"
          }
        }
      }
    }
  }

  migrate {
    max_parallel = 3
    health_check = "checks"
    min_healthy_time = "15s"
    healthy_deadline = "5m"
  }

  constraint {
    attribute = "${meta.kind}"
    set_contains = "node"
  }

  constraint {
    attribute = "${meta.customer}"
    set_contains = "shared"
  }

  vault {
    policies = ["parat"]
    change_mode = "restart"
  }
}
