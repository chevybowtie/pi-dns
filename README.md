# pi-dns

This project grew out of a desire to avoid having to sign up to a dynamic dns service. Eventually I let a few people on Reddit know about it and several asked if I could open source the code. As it's all just a harmless load of badly written python I can't see why not. If you want to make it better that would be great.


# architecture
The whole thing is done on AWS serverless services. I have used dynamodb, api gateway and lambda for the api; the website is static hosting in an S3 bucket and the domain DNS part is in Route53. The idea of the project was to get to know the AWS serverless services and how they can be used to create applications without the need to spin up server instances.

# using it
The easiest way to get started is to take a look at www.pi-dns.me which has instructions on how to use the service.
