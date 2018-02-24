import boto3
import sys
import collections
import datetime

#Set Default AWS Region
ec2 = boto3.setup_default_session(region_name='ap-south-1')
ec2 = boto3.client('ec2', region_name='ap-south-1')

def lambda_handler(event, context):



    # instance_id = "i-0d3ddaca1bda77033" #Testing

    #Invoke describe_instance api to list all instances with its prperties
    reservations = ec2.describe_instances(
        Filters=[{
        'Name': 'Project', #Instance tag name
        'Values': 'Project_123' #Instance tag value
        }]).get('Reservations', [])


    total_instances = sum(
        [[i for i in r['Instances']]
            for r in reservations ], [])

    #How long should the AMI retain on AWS EC2 Console
    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retain = 7

    add_tag = collections.defaultdict(list)

    #Format time
    create_time = datetime.datetime.now()
    date_fmt = create_time.strftime('%Y-%m-%d')


    AMI = ec2.create_image(
        InstanceId=instance['InstanceId'],
        Name="AMI - " + instance['InstanceId'] + " - " + date_fmt,
        Description="AMI by Lamdba",
        NoReboot=True,
        DryRun=False
    )

    add_tag[retain].append(AMI['ImageId'])


    for retain in add_tag.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retain)
        delete_fmt = delete_date.strftime('%m-%d-%Y')

    ec2.create_tags(
        Resources=add_tag[retain],
        Tags=[
            {'Key': 'DeleteOn', 'Value': delete_fmt},
        ]
    )
