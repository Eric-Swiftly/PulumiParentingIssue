"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import documentdb
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('cosmos_test')

ip_rules= []
for ip_address in ["104.42.195.92", "40.76.54.131", "52.176.6.30", "52.169.50.45", "52.187.184.26", "0.0.0.0"]:
    ip_rules.append(documentdb.IpAddressOrRangeArgs(ip_address_or_range=ip_address))

database_account = documentdb.DatabaseAccount(
    #opts=pulumi.ResourceOptions(parent=resource_group),
    resource_name="cosmosrutest",
    account_name="cosmosrutest",
    backup_policy=documentdb.PeriodicModeBackupPolicyArgs(periodic_mode_properties=documentdb.PeriodicModePropertiesArgs(backup_interval_in_minutes=240,
                                                                                                    backup_retention_interval_in_hours=8),
                                                type="Periodic"),
    consistency_policy=documentdb.ConsistencyPolicyArgs(default_consistency_level=documentdb.DefaultConsistencyLevel.SESSION,
                                                max_interval_in_seconds=5,
                                                max_staleness_prefix=100),
    database_account_offer_type=documentdb.DatabaseAccountOfferType.STANDARD,
    default_identity="FirstPartyIdentity",
    disable_key_based_metadata_write_access=False,
    enable_analytical_storage=False,
    kind=documentdb.DatabaseAccountKind.GLOBAL_DOCUMENT_DB,
    locations=[documentdb.LocationArgs(location_name="westus2")],
    enable_automatic_failover=False,
    enable_free_tier=True,
    enable_multiple_write_locations=False,
    identity=documentdb.ManagedServiceIdentityArgs(type=documentdb.ResourceIdentityType.NONE),
    public_network_access=documentdb.PublicNetworkAccess.ENABLED,
    ip_rules=ip_rules,
    is_virtual_network_filter_enabled=False,
    network_acl_bypass=documentdb.NetworkAclBypass.NONE,
    resource_group_name=resource_group.name,
    tags={"managed_by": "Pulumi"})

sql_database = documentdb.SqlResourceSqlDatabase(resource_name="database",
                                            #opts=pulumi.ResourceOptions(parent=database_account),
                                            account_name=database_account.name,
                                            database_name="database",
                                            options=documentdb.CreateUpdateOptionsArgs(autoscale_settings=documentdb.AutoscaleSettingsArgs(max_throughput=1000)),
                                            resource=documentdb.SqlDatabaseResourceArgs(id="database"),
                                            resource_group_name=resource_group.name,
                                            tags={"managed_by": "Pulumi"})

sqlcontainer = documentdb.SqlResourceSqlContainer(resource_name="container",
                                        #opts=pulumi.ResourceOptions(parent=sql_database),  
                                        account_name=database_account.name,
                                        container_name="container",
                                        database_name=sql_database.name,
                                        options=documentdb.CreateUpdateOptionsArgs(autoscale_settings=documentdb.AutoscaleSettingsArgs(max_throughput=1000)),
                                        resource=documentdb.SqlContainerResourceArgs(id="container",
                                                                            indexing_policy=documentdb.IndexingPolicyArgs(
                                                                                automatic=True,
                                                                                included_paths=[documentdb.IncludedPathArgs(path="/*")],
                                                                                indexing_mode=documentdb.IndexingMode.CONSISTENT,
                                                                            ),
                                                                            partition_key=documentdb.ContainerPartitionKeyArgs(
                                                                                kind=documentdb.PartitionKind.HASH,
                                                                                paths=["/id"],
                                                                            ),
                                                                            ),
                                        resource_group_name=resource_group.name,
                                        tags={"managed_by": "Pulumi"})