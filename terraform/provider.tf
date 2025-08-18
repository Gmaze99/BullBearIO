provider "aws" {
    region = "ap-south-1"
    profile = "default"
}   

terraform {
    backend "s3" {
        bucket = "bull-bear-io"
        region = "ap-south-1"
        key = "terraform.tfstate"
        encrypt = true
        use_lockfile = true
    }
}