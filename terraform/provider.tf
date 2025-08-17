provider "aws" {
    region = "ap-south-1"
    profile = "default"
}   

terraform {
    backend "s3" {
        bucket = "terraform-devops-backend-file"
        region = "ap-south-1"
        key = "terraform.tfstate"
        encrypt = true
        use_lockfile = true
    }
}