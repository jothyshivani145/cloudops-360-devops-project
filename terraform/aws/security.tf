resource "aws_security_group" "app" {
  name        = "cloudops-360-app-sg"
  description = "Security group for Flask application"
  vpc_id      = aws_vpc.cloudops.id

  tags = {
    Name = "cloudops-360-app-sg"
  }
}

resource "aws_security_group" "database" {
  name        = "cloudops-360-db-sg"
  description = "Security group for PostgreSQL"
  vpc_id      = aws_vpc.cloudops.id

  tags = {
    Name = "cloudops-360-db-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "app_http" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"

  description = "Allow public HTTP access for future web server"
}

resource "aws_vpc_security_group_ingress_rule" "database_postgres" {
  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = aws_security_group.app.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"

  description = "Allow PostgreSQL only from application security group"
}
