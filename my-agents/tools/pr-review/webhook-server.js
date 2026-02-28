const express = require('express');
const crypto = require('crypto');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

const GITHUB_WEBHOOK_SECRET = process.env.GITHUB_WEBHOOK_SECRET;
const PORT = process.env.PORT || 8080;

// Verify GitHub webhook signature
function verifySignature(payload, signature) {
    if (!GITHUB_WEBHOOK_SECRET) return true; // Skip if no secret set
    
    const hmac = crypto.createHmac('sha256', GITHUB_WEBHOOK_SECRET);
    const digest = 'sha256=' + hmac.update(payload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

// GitHub webhook endpoint
app.post('/webhook/github', (req, res) => {
    const signature = req.headers['x-hub-signature-256'];
    const payload = JSON.stringify(req.body);
    
    // Verify webhook signature
    if (!verifySignature(payload, signature)) {
        console.error('Invalid webhook signature');
        return res.status(401).send('Unauthorized');
    }
    
    const event = req.headers['x-github-event'];
    const body = req.body;
    
    console.log(`Received ${event} event`);
    
    // Handle PR events
    if (event === 'pull_request') {
        const action = body.action;
        const pr = body.pull_request;
        const repo = body.repository;
        
        // Only review on PR open or synchronize (new commits)
        if (action === 'opened' || action === 'synchronize') {
            console.log(`PR #${pr.number} ${action} in ${repo.full_name}`);
            
            // Spawn PR review agent
            const owner = repo.owner.login;
            const repoName = repo.name;
            const prNumber = pr.number;
            
            const command = `cd /root/.openclaw/workspace/my-agents && sessions_spawn --task "Review PR #${prNumber} in ${owner}/${repoName}. Title: ${pr.title}. Changes: ${pr.changed_files} files, +${pr.additions}/-${pr.deletions}. Check for security issues, code quality, and test coverage." --agent-id pr-review-agent --label "pr-review-${owner}-${repoName}-${prNumber}"`;
            
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error spawning agent: ${error}`);
                    return;
                }
                console.log(`Agent spawned: ${stdout}`);
            });
            
            res.status(200).send('Review initiated');
        } else {
            res.status(200).send('Event ignored');
        }
    } else {
        res.status(200).send('Event not handled');
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`🤖 PR Review Webhook Server running on port ${PORT}`);
    console.log(`Webhook URL: http://your-server:${PORT}/webhook/github`);
});
