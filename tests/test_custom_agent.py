from unittest.mock import patch
import scripts.custom_agent as agent

def test_run_agent_protocol_success():
    """Verify that run_agent invokes the protocol script and returns a valid result dict."""
    with patch("os.path.exists", return_value=True), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "Done: 11 ok, 0 failed, 0 skipped / 11 total"
        mock_run.return_value.returncode = 0

        result = agent.run_agent(channel="/r/lobby", count=11)

        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert "channel" in result
        assert result["channel"] == "/r/lobby"

def test_run_agent_failure_handling():
    """Verify failure state handling when protocol runner encounters an error."""
    with patch("os.path.exists", return_value=True), \
         patch(
            "subprocess.run",
            side_effect=agent.subprocess.CalledProcessError(
                1, "post.py", stderr="Network error"
            ),
        ):
        result = agent.run_agent(channel="/r/lobby")
        assert result.get("status") == "error"
        assert "message" in result
