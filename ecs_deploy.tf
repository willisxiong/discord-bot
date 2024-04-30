provider "aws" {
  region = "ap-east-1"
}

data "aws_ecs_cluster" "ecs-discord-bot-cluster" {
  cluster_name = "discord_botCluster"
}

data "aws_ecs_task_definition" "task-discord-bot" {
  task_definition = "task-for-discordbot:3"
}

data "aws_subnet" "public-1" {
  filter {
    name = "tag:Name"
    values = ["public-subnet"]
  }
}

data "aws_subnet" "public-2" {
  filter {
    name = "tag:Name"
    values = ["public-subnet-1"]
  }
}

data "aws_security_group" "web-server" {
  name = "WebServer"
}

resource "aws_ecs_service" "discord-bot" {
  name = "discord_bot_1"
  cluster = data.aws_ecs_cluster.ecs-discord-bot-cluster.id
  task_definition = data.aws_ecs_task_definition.task-discord-bot.arn
  desired_count = 1
  launch_type = "FARGATE"
  network_configuration {
    subnets = [data.aws_subnet.public-1.id, data.aws_subnet.public-2.id]
    security_groups = [data.aws_security_group.web-server.id]
    assign_public_ip = true
  }
}