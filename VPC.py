#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author : Mayank Sinha  
#Email	: sinha_mayank@hotmail.com

# Creating a sample template using python troposphere library

from troposphere import Base64, GetAtt, Equals
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

									)


			}

conditions = {
	
	"CreatePrivateSubnet1ACondition" : Equals(Ref("CreatePrivateSubnet1A"),"True"),
	"CreatePrivateSubnet1BCondition" : Equals(Ref("CreatePrivateSubnet1B"),"True")



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

# Create NAT Elsatic IP

	"NAT1EIP" : ec2.EIP(

						"NAT1EIP",
						DependsOn = "IGWAttachVPC",
						Domain = "vpc"

						),
# Create NAt Gateway

	"NATGateway1" : ec2.NatGateway(


						"NATGateway1",
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
						RouteTableId = Ref("PrivateSubnet1ARouteTable")	


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
						SubnetId = Ref("PrivateSubnet1B"),
						NetworkAclId = Ref("PrivateSubnet1BNetworkAcl")

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



