"""Perform tests on and in synthetic git repositories."""

import pathlib

import boilerplates.git_repo_tests


class GitRepoSelfTests(boilerplates.git_repo_tests.GitRepoTests):
    """Check that GitRepoTests class works."""

    def test_typical(self):
        self.git_init()
        pth = self.git_commit_new_file()
        self.git_modify_file(pth)
        pth = self.git_commit_new_file()
        self.git_modify_file(pth, add=True)
        pth = self.git_commit_new_file()
        self.git_modify_file(pth, commit=True)

    def test_clone(self):
        path = pathlib.Path(__file__).resolve().parent.parent
        self.git_clone('origin', str(path))

    def test_no_repo(self):
        self.assertIsNone(self.repo)

    def test_cleanup_nonexisting(self):
        self.git_init()
        pth = self.git_commit_new_file()
        pth.unlink()
        self.assertFalse(pth.is_file())
