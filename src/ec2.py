
RDS_SECURITY_GROUP_NAME =  "my-rds-public-sg-5"

class EC2:
    def __init__(self, client):
        self._client = client
        """:type: pyboto3.ec2"""

    def create_security_group(self):
        print("Creating RDS SG with name " + RDS_SECURITY_GROUP_NAME)
        return self._client.create_security_group(
            GroupName=RDS_SECURITY_GROUP_NAME,
            Description="RDS SG for public access",
            VpcId="vpc-1",
        )

    def add_inbound_rule_to_sg(self, security_group_id):
        print("Adding inbound access rule to security group " + security_group_id)
        self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': "Tcp",
                    'FromPort': 5432,
                    'ToPort': 5432,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] # connection availability to RDS instance
                },
            ]
        )
