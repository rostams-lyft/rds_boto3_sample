from src.client_factory import RDSClient
from src.RDS import RDS

def get_rds():
    rds_client =RDSClient().get_client()
    rds = RDS(rds_client)

    return rds

def deploy_resources():
    rds = get_rds()
    rds.create_postgresql_instance()
    print("Creating RDS PostgreSQL Instace...")


def describe_my_instances():
    print(str(get_rds().describe_instaces()))


if __name__ == '__main__':
    # deploy_resources()
    describe_my_instances()
    # modify_master_password()
    get_rds().delete_db('mypostgresdb')