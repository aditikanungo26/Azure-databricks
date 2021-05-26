# Databricks notebook source
storageAccountName = "<your storage account name>"
blobContainerName = "<blob container name>"
mountPoint = "/mnt/mountName/test"

# Application (Client) ID, Create this Client id in App Registration. Provide read/contributor permission in storage account
applicationId = dbutils.secrets.get(scope="keyvault_kv",key="clientid")

# Application (Client) Secret Key
authenticationKey = dbutils.secrets.get(scope="keyvault_kv",key="client-secret")

# Directory (Tenant) ID
tenandId = dbutils.secrets.get(scope="keyvault_kv",key="tenant-id")

endpoint = "https://login.microsoftonline.com/" + tenandId + "/oauth2/token"
source = "abfss://"+blobContainerName+"@"+storageAccountName+".dfs.core.windows.net/"

# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": applicationId,
           "fs.azure.account.oauth2.client.secret": authenticationKey,
           "fs.azure.account.oauth2.client.endpoint": endpoint}

# Mount only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)


# COMMAND ----------

# MAGIC %fs ls /mnt/mountName/test
