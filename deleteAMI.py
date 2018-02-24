import boto3
import collections
import datetime
import sys

ec2 = boto3.setup_default_session(region_name='ap-south-1')
ec2 = boto3.client('ec2', region_name='ap-south-1')
images = ec2.images.filter(Owners=["self"])

def lambda_handler(event, context):

    reservations = ec2.describe_instances(
        Filters=[{
        'Name': 'Project', #Instance tag name
        'Values': 'Project_123' #Instance tag value
        }]).get('Reservations', [])


    total_instances = sum(
        [[i for i in r['Instances']]
            for r in reservations ], [])


    to_tag = collections.defaultdict(list)

    date = datetime.datetime.now()
    date_fmt = date.strftime('%Y-%m-%d')

    imagesList = []
    flag = False
    for instance in instances:
	count = 0
        for image in images:
            if image.name.startswith('AMI - '):

	        count = count + 1

                try:
                    if image.tags is not None:
                        deletion_date = [
                            t.get('Value') for t in image.tags
                            if t['Key'] == 'DeleteOn'][0]
                        delete_date = time.strptime(deletion_date, "%m-%d-%Y")
                except IndexError:
                    deletion_date = False
                    delete_date = False

                today_time = datetime.datetime.now().strftime('%m-%d-%Y')
                today_date = time.strptime(today_time, '%m-%d-%Y')
                if delete_date <= today_date:
                    imagesList.append(image.id)
                if image.name.endswith(date_fmt):

                    flag = True


    if flag == True:
        #call Secure token service and get account id
        myAccount = boto3.client('sts').get_caller_identity()['Account']
        snapshots = ec.describe_snapshots(MaxResults=1000, OwnerIds=[myAccount])['Snapshots']


        for image in imagesList:
            #Deregister images
            amiResponse = ec2.deregister_image(
                DryRun=False,
                ImageId=image,
            )

            #deleting snapshots
            for snapshot in snapshots:
                if snapshot['Description'].find(image) > 0:
                    snap = ec.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

                else:
                    flag = False
