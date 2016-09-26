#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author : Mayank Sinha  
#Email	: sinha_mayank@hotmail.com

# Creating a sample template using python troposphere library

'''
This script will create -

1 VPC 
Option for two AvailabilityZones
Each AvailabilityZone having option of 1 Public Subnet and 2 Private Subnets 
* By default a Public Subnet will be created in AvailabilityZone 1
For each Private Subnet in each AvailabilityZone, Internet access is provided using NAT Gateway
For every additional Private subnet NACL is created with a default value of incoming from 0.0.0.0/0, which can be changed to desired CIDR 
If value is left as "false" in Parameter section then specified resource will not be created


'''


from troposphere import Base64, GetAtt, Equals, And, Or, Condition
from troposphere import Parameter, Output, Ref, Template, Tags, Join
import troposphere.ec2 as ec2


parameters = {

	"CIDRVPC" : Parameter(

					"CIDRVPC",
					Description = "Enter the CIDR Range for the VPC to be created",
					Type = "String",
					Default = "10.0.0.0/16",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

						),

	"AvailabilityZone1" : Parameter(

					"AvailabilityZone1",
					Description = "Select the first AvailabilityZone",
					Type = "String",
					Default = "ap-south-1a"

									),

	"CIDRPublicSubnet1" : Parameter(

					"CIDRPublicSubnet1",
					Description = "Enter the CIDR range for PublicSubnet1 in AZ1",
					Type = "String",
					Default = "10.0.128.0/20",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									),

	"CreatePrivateSubnet1A" : Parameter(

					"CreatePrivateSubnet1A",
					Description = "Select True or False, for creating Private Subnet 1A in AZ1",
					Type = "String",
					AllowedValues = ["True","False"],
					Default = "False"
										),

	"CIDRPrivateSubnet1A" : Parameter(

					"CIDRPrivateSubnet1A",
					Description = "Enter the CIDR block for Private Subnet 1A",
					Type = "String",
					Default = "10.0.0.0/19",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									),

	"CreatePrivateSubnet1B" : Parameter(

					"CreatePrivateSubnet1B",
					Description = "Select True or False, for creating Private Subnet 1B in AZ1",
					Type = "String",
					AllowedValues = ["True","False"],
					Default = "False"

										),

	"CIDRPrivateSubnet1B" : Parameter(

					"CIDRPrivateSubnet1B",
					Description = "Enter the CIDR block for Private Subnet 1B",
					Type = "String",
					Default = "10.0.192.0/21",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									),

	"AvailabilityZone2" : Parameter(

					"AvailabilityZone2",
					Description = "Select the second AvailabilityZone",
					Type = "String",
					Default = "ap-south-1b"

									),

	"CreatePublicSubnet2" : Parameter(

					"CreatePublicSubnet2",
					Description = "Select True or False, for creating Public Subnet 2 in AZ2",
					Type = "String",
					AllowedValues = ["True","False"],
					Default = "False"

									),

	"CIDRPublicSubnet2" : Parameter(

					"CIDRPublicSubnet2",
					Description = "Enter the CIDR range for PublicSubnet2 in AZ2",
					Type = "String",
					Default = "10.0.144.0/20",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									),

	"CreatePrivateSubnet2A" : Parameter(

					"CreatePrivateSubnet2A",
					Description = "Select True or False, for creating Private Subnet 2A in AZ2",
					Type = "String",
					AllowedValues = ["True","False"],
					Default = "False"
										),

	"CIDRPrivateSubnet2A" : Parameter(

					"CIDRPrivateSubnet2A",
					Description = "Enter the CIDR block for Private Subnet 2A",
					Type = "String",
					Default = "10.0.32.0/19",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									),

	"CreatePrivateSubnet2B" : Parameter(

					"CreatePrivateSubnet2B",
					Description = "Select True or False, for creating Private Subnet 2B in AZ2",
					Type = "String",
					AllowedValues = ["True","False"],
					Default = "False"

										),

	"CIDRPrivateSubnet2B" : Parameter(

					"CIDRPrivateSubnet2B",
					Description = "Enter the CIDR block for Private Subnet 2B",
					Type = "String",
					Default = "10.0.200.0/21",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									)



			}

conditions = {
	
	"CreatePrivateSubnet1ACondition" : Equals(Ref("CreatePrivateSubnet1A"),"True"),
	"CreatePrivateSubnet1BCondition" : Equals(Ref("CreatePrivateSubnet1B"),"True"),
	"NAT1EIPCondition" : Or(Condition("CreatePrivateSubnet1ACondition"),Condition("CreatePrivateSubnet1BCondition")),
	"CreatePublicSubnet2Condition" : Equals(Ref("CreatePublicSubnet2"),"True"),
	"CreatePrivateSubnet2ACondition" : Equals(Ref("CreatePrivateSubnet2A"),"True"),
	"CreatePrivateSubnet2BCondition" : Equals(Ref("CreatePrivateSubnet2B"),"True"),
	"AttachNAT2ACondition" : And(Condition("CreatePublicSubnet2Condition"),Condition("CreatePrivateSubnet2ACondition")),
	"AttachNAT2BCondition" : And(Condition("CreatePublicSubnet2Condition"),Condition("CreatePrivateSubnet2BCondition")),
	"NAT2EIPCondition" : Or(Condition("AttachNAT2ACondition"),Condition("AttachNAT2BCondition"))




			}

resources = {

# Add a VPC with user input CIDR block

	"VPC" : ec2.VPC(

					"VPC",
					CidrBlock = Ref("CIDRVPC"),
					EnableDnsSupport= "True",
  					EnableDnsHostnames= "True",
  					InstanceTenancy = "default",
  					Tags = Tags(
        						IoCluster=Ref("AWS::StackName"),
        						Name=Join("-",[Ref("AWS::StackName"), "VPC" ])
    						 )


				   ),

# Add InternetGateway	
	"IGW" : ec2.InternetGateway(

					"IGW",
					Tags = Tags(
								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"IGW"])

								)			

								),
# Attach IGW to VPC

	"IGWAttachVPC" : ec2.VPCGatewayAttachment(

					"IGWAttachVPC",
					VpcId = Ref("VPC"),
					InternetGatewayId = Ref("IGW")

											  ),


# Create Public Subnet 1

	"PublicSubnet1" : ec2.Subnet(

					"PublicSubnet1",
					CidrBlock = Ref("CIDRPublicSubnet1"),
					VpcId = Ref("VPC"),
					AvailabilityZone = Ref("AvailabilityZone1"),
					MapPublicIpOnLaunch = "True",
					Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PublicSubnet1"])

								)

								),

# Create Route Table for Public Subnet

	"PublicSubnetRouteTable" : ec2.RouteTable(

						"PublicSubnetRouteTable",
						VpcId = Ref("VPC"),
						Tags = Tags (

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"RouteTable"])


									)
											),

# Create route for IGW in the route table

	"PublicSubnetRoute" : ec2.Route(


						"PublicSubnetRoute",
						DependsOn = "IGWAttachVPC",
						RouteTableId = Ref("PublicSubnetRouteTable"),
						DestinationCidrBlock = "0.0.0.0/0",
						GatewayId = Ref("IGW")

									),

# Associate PublicSubnet1 to route table

	"AttachPublicSubnet1toRouteTable" : ec2.SubnetRouteTableAssociation(

						"AttachPublicSubnet1toRouteTable",
						SubnetId = Ref("PublicSubnet1"),
						RouteTableId = Ref("PublicSubnetRouteTable")


																		),
# Create Private Subnet 1A

	"PrivateSubnet1A" : ec2.Subnet(

						"PrivateSubnet1A",
						Condition = "CreatePrivateSubnet1ACondition",
						VpcId = Ref("VPC"),
						AvailabilityZone = Ref("AvailabilityZone1"),
						CidrBlock = Ref("CIDRPrivateSubnet1A"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet1A"])

								)

								),

# Create NAT Elastic IP

	"NAT1EIP" : ec2.EIP(

						"NAT1EIP",
						Condition = "NAT1EIPCondition",
						DependsOn = "IGWAttachVPC",
						Domain = "vpc"

						),
# Create NAt Gateway

	"NATGateway1" : ec2.NatGateway(


						"NATGateway1",
						Condition = "NAT1EIPCondition",
						DependsOn = "IGWAttachVPC",
						SubnetId = Ref("PublicSubnet1"),
						AllocationId = GetAtt("NAT1EIP","AllocationId")

								),
# Private Subnet 1A route Table

	"PrivateSubnet1ARouteTable" : ec2.RouteTable(

						"PrivateSubnet1ARouteTable",
						Condition = "CreatePrivateSubnet1ACondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet1ARouteTable"])

								)


												),
# Create route in PrivateSubnet1A Route Table

	"PrivateSubnet1ARoute" : ec2.Route(

						"PrivateSubnet1ARoute",
						Condition = "CreatePrivateSubnet1ACondition",
						DependsOn = "PrivateSubnet1ARouteTable",
						RouteTableId = Ref("PrivateSubnet1ARouteTable"),
						DestinationCidrBlock = "0.0.0.0/0",
						NatGatewayId = Ref("NATGateway1")

									),
# Associate private subnet 1A with the route table

	"PrivateSubnet1ARouteTableAssociation" : ec2.SubnetRouteTableAssociation(

						"PrivateSubnet1ARouteTableAssociation",
						Condition = "CreatePrivateSubnet1ACondition",
						DependsOn = "PrivateSubnet1ARoute",
						SubnetId = Ref("PrivateSubnet1A"),
						RouteTableId = Ref("PrivateSubnet1ARouteTable")	


																			),

# Create Private Subnet 1B

	"PrivateSubnet1B" : ec2.Subnet(

						"PrivateSubnet1B",
						Condition = "CreatePrivateSubnet1BCondition",
						VpcId = Ref("VPC"),
						AvailabilityZone = Ref("AvailabilityZone1"),
						CidrBlock = Ref("CIDRPrivateSubnet1B"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet1B"])

								)

								),

# Private Subnet 1B route Table

	"PrivateSubnet1BRouteTable" : ec2.RouteTable(

						"PrivateSubnet1BRouteTable",
						Condition = "CreatePrivateSubnet1BCondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet1BRouteTable"])

								)

												),
# Create route in PrivateSubnet1B Route Table

	"PrivateSubnet1BRoute" : ec2.Route(

						"PrivateSubnet1BRoute",
						Condition = "CreatePrivateSubnet1BCondition",
						DependsOn = "PrivateSubnet1BRouteTable",
						RouteTableId = Ref("PrivateSubnet1BRouteTable"),
						DestinationCidrBlock = "0.0.0.0/0",
						NatGatewayId = Ref("NATGateway1")

									),
# Associate private subnet 1B with the route table

	"PrivateSubnet1BRouteTableAssociation" : ec2.SubnetRouteTableAssociation(

						"PrivateSubnet1BRouteTableAssociation",
						Condition = "CreatePrivateSubnet1BCondition",
						DependsOn = "PrivateSubnet1BRoute",
						SubnetId = Ref("PrivateSubnet1B"),
						RouteTableId = Ref("PrivateSubnet1BRouteTable")	


																			),
# Create A NACL for Private Subnet 1B

	"PrivateSubnet1BNetworkAcl" : ec2.NetworkAcl(

						"PrivateSubnet1BNetworkAcl",
						Condition = "CreatePrivateSubnet1BCondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"NACLPrivateSubnet1B"])

								)


												),
# Create Inbound rules for NACL connected to Private Subnet 1B

	"PrivateSubnet1BNetworkAclEntryInbound" : ec2.NetworkAclEntry(

						"PrivateSubnet1BNetworkAclEntryInbound",
						Condition = "CreatePrivateSubnet1BCondition",
						CidrBlock = "10.0.0.0/16",
						Egress = "true",
						NetworkAclId = Ref("PrivateSubnet1BNetworkAcl"),
						Protocol = "-1",
						RuleAction = "allow",
						RuleNumber = "100"

																),

# Associate the created NACL with the Private Subnet 1B

	"PrivateSubnet1BNetworkAclAssociation" : ec2.SubnetNetworkAclAssociation(

						"PrivateSubnet1BNetworkAclAssociation",
						Condition = "CreatePrivateSubnet1BCondition",
						SubnetId = Ref("PrivateSubnet1B"),
						NetworkAclId = Ref("PrivateSubnet1BNetworkAcl")

																			),

#Create Public Subnet 2 in AZ2

"PublicSubnet2" : ec2.Subnet(

					"PublicSubnet2",
					Condition = "CreatePublicSubnet2Condition",
					CidrBlock = Ref("CIDRPublicSubnet2"),
					VpcId = Ref("VPC"),
					AvailabilityZone = Ref("AvailabilityZone2"),
					MapPublicIpOnLaunch = "True",
					Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PublicSubnet2"])

								)

								),

# Associate PublicSubnet2 to route table

	"AttachPublicSubnet2toRouteTable" : ec2.SubnetRouteTableAssociation(

						"AttachPublicSubnet2toRouteTable",
						Condition = "CreatePublicSubnet2Condition",
						SubnetId = Ref("PublicSubnet2"),
						RouteTableId = Ref("PublicSubnetRouteTable")


																		),
# Create Private Subnet 2A

	"PrivateSubnet2A" : ec2.Subnet(

						"PrivateSubnet2A",
						Condition = "CreatePrivateSubnet2ACondition",
						VpcId = Ref("VPC"),
						AvailabilityZone = Ref("AvailabilityZone2"),
						CidrBlock = Ref("CIDRPrivateSubnet2A"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet2A"])

								)

								),

# Create NAT2 Elsatic IP

	"NAT2EIP" : ec2.EIP(

						"NAT2EIP",
						Condition = "NAT2EIPCondition",
						DependsOn = "IGWAttachVPC",
						Domain = "vpc"

						),
# Create NAT  Gateway 2

	"NATGateway2" : ec2.NatGateway(


						"NATGateway2",
						DependsOn = "IGWAttachVPC",
						Condition = "NAT2EIPCondition",
						SubnetId = Ref("PublicSubnet2"),
						AllocationId = GetAtt("NAT2EIP","AllocationId")

								),
# Private Subnet 2A route Table

	"PrivateSubnet2ARouteTable" : ec2.RouteTable(

						"PrivateSubnet2ARouteTable",
						Condition = "AttachNAT2ACondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet2ARouteTable"])

								)


												),
# Create route in PrivateSubnet2A Route Table

	"PrivateSubnet2ARoute" : ec2.Route(

						"PrivateSubnet2ARoute",
						Condition = "AttachNAT2ACondition",
						DependsOn = "PrivateSubnet2ARouteTable",
						RouteTableId = Ref("PrivateSubnet2ARouteTable"),
						DestinationCidrBlock = "0.0.0.0/0",
						NatGatewayId = Ref("NATGateway2")

									),
# Associate private subnet 2A with the route table

	"PrivateSubnet2ARouteTableAssociation" : ec2.SubnetRouteTableAssociation(

						"PrivateSubnet2ARouteTableAssociation",
						Condition = "AttachNAT2ACondition",
						DependsOn = "PrivateSubnet2ARoute",
						SubnetId = Ref("PrivateSubnet2A"),
						RouteTableId = Ref("PrivateSubnet2ARouteTable")	


																			),

# Create Private Subnet 2B

	"PrivateSubnet2B" : ec2.Subnet(

						"PrivateSubnet2B",
						Condition = "CreatePrivateSubnet2BCondition",
						VpcId = Ref("VPC"),
						AvailabilityZone = Ref("AvailabilityZone2"),
						CidrBlock = Ref("CIDRPrivateSubnet2B"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet2B"])

								)

								),

# Private Subnet 2B route Table

	"PrivateSubnet2BRouteTable" : ec2.RouteTable(

						"PrivateSubnet2BRouteTable",
						Condition = "AttachNAT2BCondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"PrivateSubnet2BRouteTable"])

								)

												),
# Create route in PrivateSubnet2B Route Table

	"PrivateSubnet2BRoute" : ec2.Route(

						"PrivateSubnet2BRoute",
						Condition = "AttachNAT2BCondition",
						DependsOn = "PrivateSubnet2BRouteTable",
						RouteTableId = Ref("PrivateSubnet2BRouteTable"),
						DestinationCidrBlock = "0.0.0.0/0",
						NatGatewayId = Ref("NATGateway2")

									),
# Associate private subnet 2B with the route table

	"PrivateSubnet2BRouteTableAssociation" : ec2.SubnetRouteTableAssociation(

						"PrivateSubnet2BRouteTableAssociation",
						Condition = "AttachNAT2BCondition",
						DependsOn = "PrivateSubnet2BRoute",
						SubnetId = Ref("PrivateSubnet2B"),
						RouteTableId = Ref("PrivateSubnet2ARouteTable")	


																			),
# Create A NACL for Private Subnet 2B

	"PrivateSubnet2BNetworkAcl" : ec2.NetworkAcl(

						"PrivateSubnet2BNetworkAcl",
						Condition = "CreatePrivateSubnet2BCondition",
						VpcId = Ref("VPC"),
						Tags = Tags(

								IoCluster = Ref("AWS::StackName"),
								Name = Join("-",[Ref("AWS::StackName"),"NACLPrivateSubnet2B"])

								)


												),
# Create Inbound rules for NACL connected to Private Subnet 2B

	"PrivateSubnet2BNetworkAclEntryInbound" : ec2.NetworkAclEntry(

						"PrivateSubnet2BNetworkAclEntryInbound",
						Condition = "CreatePrivateSubnet2BCondition",
						CidrBlock = "0.0.0.0/0",
						Egress = "true",
						NetworkAclId = Ref("PrivateSubnet2BNetworkAcl"),
						Protocol = "-1",
						RuleAction = "allow",
						RuleNumber = "100"

																),

# Associate the created NACL with the Private Subnet 2B

	"PrivateSubnet2BNetworkAclAssociation" : ec2.SubnetNetworkAclAssociation(

						"PrivateSubnet2BNetworkAclAssociation",
						Condition = "CreatePrivateSubnet2BCondition",
						SubnetId = Ref("PrivateSubnet2B"),
						NetworkAclId = Ref("PrivateSubnet2BNetworkAcl")

																			)



			}



t = Template()

for p in parameters.values():
	t.add_parameter(p)

for k in conditions:
	t.add_condition(k, conditions[k])

for r in resources.values():
	t.add_resource(r)

print (t.to_json())



