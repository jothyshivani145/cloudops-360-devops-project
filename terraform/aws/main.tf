resource "aws_vpc" "cloudops" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "cloudops-360-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.cloudops.id
  cidr_block              = "10.20.1.0/24"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = false

  tags = {
    Name = "cloudops-360-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.cloudops.id
  cidr_block        = "10.20.2.0/24"
  availability_zone = "eu-west-2b"

  tags = {
    Name = "cloudops-360-private-subnet"
  }
}

resource "aws_internet_gateway" "cloudops" {
  vpc_id = aws_vpc.cloudops.id

  tags = {
    Name = "cloudops-360-igw"
  }
}
