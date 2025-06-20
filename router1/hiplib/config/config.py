config = {
	"switch": {
		"l2interface": "r1-eth0",
		"mesh": "hiplib/config/mesh",
                "source_ip": "192.168.3.1"
	},
	"network": {
		"tun_name": "hip0",                                    # Interface name
		"mtu": 1400                                            # MTU
	},
	"security": {
		"public_key": "hiplib/config/public.pem",                   # ECDSA/RSA public key
		"private_key": "hiplib/config/private.pem",                 # ECDSA/RSA private key
		"sig_alg": 0x5,                                        # RSA 5, ECDSA 7, ECDSA LOW 9, DSA 3
		"hash_alg": 0x1,                                       # SHA-256 0x1, SHA-384 0x2, SHA-1 0x3
		# If signature algorithm is ECDSA,
		# then HASH algorithm should be SHA-384,
		# HASH algorithm is the one that is used
		# to compute the HMAC, as well as to construct HIT
		"puzzle_difficulty": 0x10,                             # 16 bits
		"puzzle_lifetime_exponent": 37,                        # 32 seconds
		# Currently DH can be used ONLY with ECDSA because
		# fragmentation does not work
		"supported_DH_groups": [0x4, 0x9, 0x8, 0x3, 0x7, 0xa], # ECDHNIST521 (0x9), ECDHNIST384 (0x8), ECDHNIST256 (0x7), DH5 (0x3), DH15 (0x4), ECDHSECP160R1 (0xa)
		"supported_ciphers": [0x1],                  # NULL (0x1), AES128CBC (0x2), AES256CBC (0x4)
		"supported_hit_suits": [0x10, 0x20, 0x30],             # SHA256 (0x1), SHA384 (0x2), SHA1 (0x3)
		"supported_transports": [0x0FFF],                      # IPSec
		"supported_signatures": [0x5, 0x7, 0x9],               # DSA (0x3), RSA (0x5), ECDSA (0x7), ECDSA_LOW (0x9)
		"supported_esp_transform_suits": [0x7]       # NULL with HMAC-SHA-256 (0x7), AES-128-CBC with HMAC-SHA-256 (0x8), AES-256-CBC with HMAC-SHA-256 (0x9)
	},
	"resolver": {
		"hosts_file": "hiplib/config/hosts",
		"domain_identifier": {                                 # Domain identifier type and value
			"type": 0x2,                                       # FQDN 0x1, NAI 0x2
			"value": "dmitriy.kuptsov@strangebit.com"          # NAI value
		}
	},
	"general": {
		"i1_timeout_s": 20,                                    # I1 timeout
		"i1_retries": 3,                                       # I1 retrues
		"i2_retries": 3,                                       # I2 retries
		"i2_timeout_s": 20,                                    # I2 timeout
		"update_timeout_s": 120,                               # Update send interval
		"close_timeout_s": 30,                                 # Close timeout
		"UAL": 120,                                            # Unused Association Lifetime (UAL)
		"MSL": 120,                                            # Maximum Segment Lifetime (MSL)
		"EC": 120,                                             # Exchange Complete (EC) timeout
		"failed_timeout": 120,                                 # Failed timeout
		"rekey_after_packets": 100                             # When to rekey the association
	},
	"firewall": {
		"rules_file": "hiplib/config/rules"
	}
}

