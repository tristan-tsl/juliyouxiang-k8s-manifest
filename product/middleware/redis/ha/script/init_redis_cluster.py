import os
import socket


def init_redis_cluster():
    env_dist = os.environ
    # get the env
    redis_deployment_name = env_dist.get("REDIS_DEPLOYMENT_NAME")
    redis_service_name = env_dist.get("REDIS_SERVICE_NAME")
    redis_namespace_name = env_dist.get("REDIS_NAMESPACE_NAME")
    redis_port = env_dist.get("REDIS_PORT")
    redis_slave_num = env_dist.get("REDIS_SLAVE_NUM")
    redis_cluster_start = env_dist.get("REDIS_CLUSTER_START")
    redis_cluster_end = env_dist.get("REDIS_CLUSTER_END")

    # set the default value
    if not redis_deployment_name:
        redis_deployment_name = "redis-app"
    if not redis_service_name:
        redis_service_name = "redis-service"
    if not redis_namespace_name:
        redis_namespace_name = "middleware"
    if not redis_port:
        redis_port = 6379
    if not redis_slave_num:
        redis_slave_num = 1
    if not redis_cluster_start:
        redis_cluster_start = 1
    if not redis_cluster_end:
        redis_cluster_end = 6

    # init the redis cluster by redis-trib
    def init_redis_master(master_url):
        os.system("redis-trib.py create %s" % master_url)

    def init_redis_slave(master_url, slave_url):
        os.system("redis-trib.py replicate --master-addr %s --slave-addr %s" % (master_url, slave_url))

    # gen ms cluster info
    redis_cluster_index = redis_cluster_start - 1
    redis_master_url = None
    while redis_cluster_index < redis_cluster_end:
        # get the ip from the domain name, for example: redis-app-0.redis-service.%s.svc.cluster.local
        redis_cluster_domain_name = "%s-%s.%s.%s.svc.cluster.local" % (
            redis_deployment_name, redis_cluster_index, redis_service_name, redis_namespace_name)
        redis_cluster_url = socket.gethostbyname(redis_cluster_domain_name) + ":" + redis_port
        if redis_cluster_index % (redis_slave_num + 1) == 0:
            init_redis_master(redis_cluster_url)
            redis_master_url = redis_cluster_url
        else:
            init_redis_slave(redis_master_url, redis_cluster_url)
        redis_cluster_index += 1


if __name__ == '__main__':
    init_redis_cluster()
