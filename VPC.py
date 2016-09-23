#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author : Mayank Sinha  
#Email	: sinha_mayank@hotmail.com

# Creating a sample template using python troposphere library

from troposphere import Base64, GetAtt
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
					Default = "us-west-2a"

									),

	"CIDRPublicSubnet1" : Parameter(

					"CIDRPublicSubnet1",
					Description = "Enter the CIDR range for PublicSubnet1 in AZ1",
					Type = "String",
					Default = "10.0.128.0/20",
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$"

									)


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

								)

			}


t = Template()

for p in parameters.values():
	t.add_parameter(p)

for r in resources.values():
	t.add_resource(r)

print (t.to_json())



