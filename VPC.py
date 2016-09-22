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
					AllowedPattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]|[1-2][0-9]|3[0-2]))$",

						)


			}

resources = {


	"VPC" : ec2.VPC(

					"VPC",
					CidrBlock = Ref("CIDRVPC"),
					EnableDnsSupport= "True",
  					EnableDnsHostnames= "True",
  					InstanceTenancy = "default"
  					Tags = Tags(
        						IoCluster=Ref("AWS::StackName"),
        						Name=Join("-",[Ref("AWS::StackName"), "VPC" ])
    						 ),


				   )

			}


t = Template()

for p in parameters.values():
	t.add_parameter(p)

for r in resources.values():
	t.add_resource(r)

print (t.to_json())



