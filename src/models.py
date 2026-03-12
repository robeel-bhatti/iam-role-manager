from pydantic import BaseModel

class Permission(BaseModel):
    Effect: str
    Action: list[str]
    Resource: str

class PolicyDocument(BaseModel):
    Version: str
    Statement: list[Permission]

class Policy(BaseModel):
    PolicyName: str
    PolicyDocument: PolicyDocument

class Tag(BaseModel):
    Key: str
    Value: str

class Role(BaseModel):
    RoleName: str
    Description: str
    AssumeRolePolicyDocument: PolicyDocument
    ManagedPolicyArns: list[str]
    Policies: list[Policy] 
    Tags: list[Tag]

