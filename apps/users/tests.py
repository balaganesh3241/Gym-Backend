from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from apps.organizations.models import Organization, Branch
from apps.users.models import User

class UserOrganizationBranchIntegrityTest(TestCase):
    def setUp(self):
        self.org_a = Organization.objects.create(name="Org A")
        self.org_b = Organization.objects.create(name="Org B")
        self.branch_a = Branch.objects.create(organization=self.org_a, name="Branch A", code="A1")
        self.branch_b = Branch.objects.create(organization=self.org_b, name="Branch B", code="B1")

    def test_valid_user(self):
        # TEST 1 & 3 - Valid
        user = User(email="test1@example.com", organization=self.org_a, branch=self.branch_a)
        user.full_clean()
        user.save()
        self.assertEqual(user.organization, self.org_a)

    def test_invalid_user_model_validation(self):
        # TEST 2 - Invalid (Model level)
        user = User(email="test2@example.com", organization=self.org_a, branch=self.branch_b)
        with self.assertRaises(ValidationError):
            user.full_clean()
            
        with self.assertRaises(ValidationError):
            user.save()

    def test_organization_only_user(self):
        # TEST 4
        user = User(email="test4@example.com", organization=self.org_a, branch=None)
        user.full_clean()
        user.save()
        self.assertEqual(user.organization, self.org_a)
        self.assertIsNone(user.branch)

    def test_no_organization_no_branch_user(self):
        # TEST 5
        user = User(email="test5@example.com", organization=None, branch=None)
        user.full_clean()
        user.save()
        self.assertIsNone(user.organization)
        self.assertIsNone(user.branch)

    def test_branch_without_organization_auto_assigns(self):
        # Test clean method auto-assignment logic
        user = User(email="test6@example.com", branch=self.branch_a)
        user.clean()
        self.assertEqual(user.organization, self.org_a)

    def test_existing_valid_records(self):
        # TEST 6 - existing records
        user = User.objects.create(email="test7@example.com", organization=self.org_a, branch=self.branch_a)
        user.refresh_from_db()
        self.assertEqual(user.organization, self.org_a)
