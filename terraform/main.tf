provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "flask_app" {
  ami = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name = "your-key-name"

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install docker -y
              sudo service docker start
              docker run -d -p 80:5000 your-dockerhub/flask-obsolete:latest
              EOF
}
