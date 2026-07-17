from pathlib import Path
import re
import unittest


WORKFLOW = Path(".github/workflows/auto-add-to-project.yml")
SANITY_WORKFLOW = Path(".github/workflows/workflow-sanity.yml")


class RepositoryModuleMappingTest(unittest.TestCase):
    def test_octo_docs_html_maps_to_server(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        mapping_block = re.search(
            r"const REPO_MODULE = \{(?P<body>.*?)^\s*\};",
            workflow,
            flags=re.MULTILINE | re.DOTALL,
        )

        self.assertIsNotNone(mapping_block, "REPO_MODULE mapping block is missing")
        mappings = dict(
            re.findall(
                r"^\s*'([^']+)':\s*'([^']+)',\s*$",
                mapping_block.group("body"),
                flags=re.MULTILINE,
            )
        )
        self.assertEqual(mappings.get("octo-docs-html"), "server")

    def test_contract_job_only_runs_in_central_repository(self) -> None:
        workflow = SANITY_WORKFLOW.read_text(encoding="utf-8")
        contracts_job = re.search(
            r"^  contracts:\n(?P<body>.*?)(?=^  [a-z][a-z0-9-]*:\n)",
            workflow,
            flags=re.MULTILINE | re.DOTALL,
        )

        self.assertIsNotNone(contracts_job, "contracts job is missing")
        self.assertIn(
            "if: github.repository == 'Mininglamp-OSS/.github'",
            contracts_job.group("body"),
        )


if __name__ == "__main__":
    unittest.main()
