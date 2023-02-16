import boto3
from botocore.exceptions import NoCredentialsError
import logging

"""this is a class which helps in performing S3Bucket operations
"""


class s3_bucket_util:

    @staticmethod
    def upload_to_aws(access_key, secret_key, local_file, bucket, s3_file):
        """
        This function uploads a file to an S3 bucket

        :param access_key: The access key for your AWS account
        :param secret_key: The secret key of the AWS account
        :param local_file: The local file path to the file you want to upload
        :param bucket: The name of the bucket you want to upload to
        :param s3_file: The file name that will be created in the bucket
        :return: a boolean value.
        """

        logger = logging.getLogger('ineuron')
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

        try:
            s3.upload_file(local_file, bucket, s3_file)
            logger.info("Upload to S3 Bucket Successful")
            return True
        except FileNotFoundError as e:
            logger.info("The S3 Bucket file not  found", e)
            return False
        except NoCredentialsError as e:
            logger.info("S3 Bucket Credentials wrong", e)
            return False
