# Distributed Machine Learning

## Summary

1. [Introduction](#introduction)
1. [Requirements](#requirements)


## Introduction

This proof-of-concept distributed machine learning solution targets a highly specific and recurring challenge frequently encountered during my work at TuringUSP. **Within the scope of my ongoing project**, our machine learning pipelines demand substantial computational resources. Rather than opting for cloud computing, our preference **in this case** is to execute these tasks exclusively on our own local machines. Each parameter within a defined set requires substantial computational resources, and attempting to execute them all on my modest machine yields unacceptably long processing times.

On the bright side, the computations are independent of one another. With this in mind, a straightforward solution is to partition the parameter set and delegate each subset to my colleagues for execution in their machines. However, managing this task manually proves both tedious and inefficient.

The current project introduces a streamlined approach to task management. It enables us to register tasks along with their associated parameter sets. By automating the assignment of subsets to individual colleagues and persisting the results, we hope to simplify and accelerate our workflow significantly.

While more robust tools like Celery, RabbitMQ, or Kafka could be used for this purpose, I'm opting for a simpler approach to avoid overengineering. If the system proves highly useful in the future, I can revisit it and enhance it as needed.

Trunk-based development was chosen in this scenario since I'll be the only one working on this project for now. If it becomes more complex and more people start working on it, GitFlow will be favored.

## Requirements

