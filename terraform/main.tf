module "vpc" {
  source = "./vpc"
}

module "ec2" {
  source = "./ec2"
  vpc_id = module.vpc.vpc_id
  subnet_id = module.vpc.subnet_ids
  key = "playground"
  ec2_ingress_rule = {
    "all" = {
      port = 0
      protocol = "-1"
      cidr_block = ["0.0.0.0/0"]
      description = "Allowing All Traffic"
    }
    "SSH" = {
      port = 22
      protocol = "tcp"
      cidr_block = ["0.0.0.0/0"]
      description = "Allowing SSH traffic"
    }
  }
}

module "eks" {
  source = "./eks"
  vpc_id = module.vpc.vpc_id
  sub_ids = module.vpc.subnet_ids
  eks_ingress_rule = {
    "all" = {
      port = 0
      protocol = "-1"
      cidr_block = ["0.0.0.0/0"]
      description = "Allowing All Traffic"
    }
    "SSH" = {
      port = 22
      protocol = "tcp"
      cidr_block = ["0.0.0.0/0"]
      description = "Allowing SSH traffic"
    }
  }
  depends_on = [ module.ec2 ]
}
