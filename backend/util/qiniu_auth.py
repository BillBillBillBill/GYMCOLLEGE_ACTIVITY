from config import QN_AK, QN_SK
import qiniu

q = qiniu.Auth(QN_AK, QN_SK)
bucket = qiniu.BucketManager(q)
bucket_name = "gymcollege"


def get_file(key):
    ret, info = bucket.stat(bucket_name, key)
    print(info)

def get_file_linl(key, domain="http://7xvx8l.com1.z0.glb.clouddn.com"):
    return "%s/%s" % (domain, key)
