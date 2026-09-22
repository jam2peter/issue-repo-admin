import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from repo_admin import load_config, parse_command, provision


class FakeRest:
    def __init__(self, responses):
        self.responses=list(responses)
        self.calls=[]
    def request(self, url, method="GET", payload=None):
        self.calls.append((url,method,payload))
        return self.responses.pop(0)


CFG={
    "owner":"example-owner",
    "owner_type":"user",
    "allowed_author_associations":["OWNER"],
    "default_description":"Managed by Issue Repo Admin",
    "auto_init":True,
    "has_issues":True,
    "has_projects":True,
    "has_wiki":False,
    "delete_branch_on_merge":True,
}


class Tests(unittest.TestCase):
    def test_example_config(self):
        self.assertEqual(load_config(str(ROOT/"repo-admin.example.json"))["owner"], "example-owner")

    def test_command(self):
        cmd=parse_command("/repo-admin create demo public")
        self.assertEqual((cmd.name,cmd.visibility),("demo","public"))

    def test_invalid_command(self):
        with self.assertRaises(ValueError):
            parse_command("/repo-admin delete demo")

    def test_association_denied_without_api(self):
        api=FakeRest([])
        result=provision(CFG,"CONTRIBUTOR",parse_command("/repo-admin create demo public"),api)
        self.assertEqual(result["error"],"author_association_denied")
        self.assertEqual(api.calls,[])

    def test_create_personal_repo_requires_matching_identity(self):
        api=FakeRest([
            (404,{"message":"Not Found"}),
            (200,{"login":"example-owner"}),
            (201,{"full_name":"example-owner/demo","private":False,"html_url":"https://github.com/example-owner/demo"}),
        ])
        result=provision(CFG,"OWNER",parse_command("/repo-admin create demo public"),api)
        self.assertTrue(result["ok"])
        self.assertTrue(result["created"])
        self.assertEqual(api.calls[1][0],"https://api.github.com/user")

    def test_owner_mismatch_denied(self):
        api=FakeRest([(404,{}),(200,{"login":"other-user"})])
        result=provision(CFG,"OWNER",parse_command("/repo-admin create demo public"),api)
        self.assertEqual(result["error"],"authenticated_user_owner_mismatch")
        self.assertEqual(len(api.calls),2)

    def test_existing_is_idempotent(self):
        api=FakeRest([(200,{"full_name":"example-owner/demo","private":False})])
        result=provision(CFG,"OWNER",parse_command("/repo-admin create demo public"),api)
        self.assertTrue(result["ok"])
        self.assertFalse(result["created"])

    def test_visibility_mismatch_denied(self):
        api=FakeRest([(200,{"full_name":"example-owner/demo","private":True})])
        result=provision(CFG,"OWNER",parse_command("/repo-admin create demo public"),api)
        self.assertEqual(result["error"],"visibility_mismatch_refusing_mutation")


if __name__=="__main__":
    unittest.main()
