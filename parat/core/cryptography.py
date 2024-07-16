from django.conf import settings
from django.contrib.auth.hashers import Argon2PasswordHasher


class CustomisedArgon2PasswordHasher(Argon2PasswordHasher):
    """
    best practices according to
    <https://password-hashing.net/argon2-specs.pdf> §6.4, §8, §9 (2015)
    and <https://tools.ietf.org/html/draft-irtf-cfrg-argon2#section-4> §4 (2018).
    """

    # ❯ hyperfine -w2 -r5 "echo -n some_pass_phrase|argon2 16_salty_octets_ -id -t 1 -m 20 -p 8"
    # Type:           Argon2id
    # Iterations:     1
    # Memory:         1048576 KiB
    # Parallelism:    8
    # Hash:           995a12f8f3cbfa53834e2ad65ccb6e654a3bb855b8968bb90c1a2777ff0e584f
    # Encoded:        $argon2id$v=19$m=1048576,t=1,p=8$MTZfc2FsdHlfb2N0ZXRzXw$mVoS+PPL+lODTirWXMtuZUo7uFW4lou5DBond/8OWE8

    time_cost = settings.SETUP.CRYPTOGRAPHY_ARGON2_TIMECOST
    memory_cost = settings.SETUP.CRYPTOGRAPHY_ARGON2_MEMORYCOST
    parallelism = settings.SETUP.CRYPTOGRAPHY_ARGON2_NPROC
