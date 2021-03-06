"""Test PDT tasks."""
import mock
import pytest

from pdt.core.tasks import (
    fetch_cases,
    send_emails,
    update_case_from_fogbugz,
    update_case_to_fogbugz,
    update_cases_from_fogbugz,
    update_cases_to_fogbugz,
)
from pdt.core.models import (
    DeploymentReport,
    MigrationReport,
)


def test_update_case_to_fogbugz(
        transactional_db, mocked_fogbugz, case_factory, migration_factory, deployment_report_factory,
        migration_report_factory, instance):
    """Test update case to fogbugz task."""
    deployed_case = case_factory(tags=['deployed-{0}'.format(instance.name)], ci_project=instance.ci_projects.first())
    migration_factory(case=deployed_case)
    mocked_case = mocked_fogbugz.return_value.search.return_value.cases.find.return_value
    mocked_case.attrs = dict(ixbug=deployed_case.id)
    mocked_case.sfixfor.string = '1516'
    mocked_case.dtfixfor.string = '2015-01-18T23:00:00Z'
    mocked_case.dtlastupdated.string = '2015-01-18T23:00:00Z'
    mocked_case.stitle.string = 'Some title'
    mocked_case.soriginaltitle.string = 'Some original title'
    mocked_case.cixproject.string = 'some-ci-project'
    mocked_case.sproject.string = 'Some project'
    mocked_case.sarea.string = 'Some area'
    deployment_report_factory(
        status=DeploymentReport.STATUS_DEPLOYED,
        instance=instance)
    migration_report_factory(
        status=MigrationReport.STATUS_APPLIED,
        migration=deployed_case.migration,
        instance=instance)
    not_deployed_case = case_factory(ci_project=instance.ci_projects.all()[0])
    edits = deployed_case.edits.all()
    assert edits
    assert not not_deployed_case.edits.all()
    update_case_to_fogbugz(deployed_case.id)
    edits = not_deployed_case.edits.all()
    assert len(edits) == 0


@mock.patch('pdt.core.tasks.update_case_to_fogbugz')
def test_update_cases_to_fogbugz(mocked_update, transactional_db, case):
    """Test update cases to fogbugz task."""
    update_cases_to_fogbugz()
    mocked_update.apply_async.assert_called_once_with(kwargs=dict(case_id=case.id))


def test_update_case_from_fogbugz(
        transactional_db, mocked_fogbugz, case_factory, instance, case):
    """Test update case from fogbugz task."""
    mocked_case = mocked_fogbugz.return_value.search.return_value.cases.find.return_value
    mocked_case.attrs = dict(ixbug=case.id)
    mocked_case.sfixfor.string = '1516'
    mocked_case.dtfixfor.string = '2015-01-18T23:00:00Z'
    mocked_case.dtlastupdated.string = '2015-01-18T23:00:00Z'
    mocked_case.stitle.string = 'Some title'
    mocked_case.soriginaltitle.string = 'Some original title'
    mocked_case.cixproject.string = 'some-ci-project'
    mocked_case.sproject.string = 'Some project'
    mocked_case.sarea.string = 'Some area'
    mocked_case.revision.string = '123123'
    update_case_from_fogbugz(case.id)
    case.refresh_from_db()
    assert case.title == 'Some title'
    assert case.revision == '123123'


@mock.patch('pdt.core.tasks.update_case_from_fogbugz')
@pytest.mark.parametrize('case__release', [None])
def test_update_cases_from_fogbugz(mocked_update, transactional_db, case):
    """Test update cases from fogbugz task."""
    update_cases_from_fogbugz()
    mocked_update.apply_async.assert_called_once_with(kwargs=dict(case_id=case.id))


@mock.patch('pdt.core.tasks.update_case_from_fogbugz')
def test_fetch_cases(mocked_update, mocked_fogbugz, transactional_db, case):
    """Test fetch cases from fogbugz task."""
    mocked_case = mock.Mock()
    mocked_fogbugz.return_value.search.return_value.findAll.return_value = [mocked_case]
    mocked_case.attrs = dict(ixbug=case.id)
    mocked_case.sfixfor.string = '1516'
    mocked_case.dtfixfor.string = '2015-01-18T23:00:00Z'
    mocked_case.dtlastupdated.string = '2015-01-18T23:00:00Z'
    mocked_case.stitle.string = 'Some title'
    mocked_case.soriginaltitle.string = 'Some original title'
    mocked_case.cixproject.string = 'some-ci-project'
    mocked_case.sproject.string = 'Some project'
    mocked_case.sarea.string = 'Some area'
    fetch_cases()
    mocked_update.apply_async.assert_called_once_with(kwargs=dict(case_id=case.id))


@mock.patch('pdt.core.tasks.call_command')
def test_send_emails(mocked_call_command, transactional_db):
    """Test send emails task."""
    send_emails()
    mocked_call_command.assert_called_once_with('send_queued_mail', interactive=False)
