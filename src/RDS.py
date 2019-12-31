from src.client_factory import EC2Client
from src.ec2 import EC2

RDS_DB_SUBNET_NAME = 'my-rds-subnet-group-4'

class RDS:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.rds """

    def create_postgresql_instance(self):
        print("Creating Amazon RDS Postgresql DB Instance...")
        security_group_id = self.create_db_security_group_and_add_rules()

        self.create_db_subnet_group()

        self._client.create_db_instance(
            DBName='MyPostgresSQLDB',
            DBInstanceIdentifier='mypostgresdb',
            DBInstanceClass='db.t2.micro',
            Engine='postgres',
            EngineVersion='9.6.6',
            Port=5432,
            MasterUsername='**',
            MasterUserPassword='**',
            AllocatedStorage=20,
            MultiAZ=False,
            StorageType='gp2',
            PubliclyAccessible=True,
            VpcSecurityGroupIds= [security_group_id],
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'test-PostgreSQL-Instance'
                }
            ]
        )

    def create_db_subnet_group(self):
        print("Creating RDS DB subnet group " + RDS_DB_SUBNET_NAME)

        self._client.create_db_subnet_group(
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            DBSubnetGroupDescription='Subnet group for RDS DB',
            SubnetIds=['subnet-1', 'subnet-2', 'subnet-3', 'subnet-4']
        )

    def create_db_security_group_and_add_rules(self):
        ec2_client = EC2Client().get_client()
        ec2 = EC2(ec2_client)

        # creating security group
        security_group = ec2.create_security_group()

        # get id of SG
        security_group_id = security_group['GroupId']

        print("Created RDS security group with id " + security_group_id)

        # add public access rule to SG
        ec2.add_inbound_rule_to_sg(security_group_id)

        print("Added inbound public access rul to sg " + security_group_id)

        return security_group_id

    def describe_instaces(self):
        print("Describing all RDS instances...")
        return self._client.describe_db_instances()

    def modify_master_user_password(self, db_identifier, new_password):
        print("Modifying master user password...")
        self._client.modify_db_instace(
            DBInstanceIdentifier=db_identifier,
            MasterUserPassword=new_password,
        )

    def take_backup_of_db_instance(self):
        return self._client.create_db_snapshot()

    def delete_db(self, db_identifier):
        print("Deleting RDS instance with name " + db_identifier)
        return self._client.delete_db_instance(
            DBInstanceIdentifier=db_identifier,
            SkipFinalSnapshot=True,
        )
