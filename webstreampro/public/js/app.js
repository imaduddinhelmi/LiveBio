let parsedBroadcasts = [];
let clientSecretUploaded = false;

window.onload = function() {
    updateRedirectUriDisplay();
    checkAuthStatus();
    checkUrlParams();
};

function updateRedirectUriDisplay() {
    const port = window.location.port || '3000';
    const redirectUri = `http://localhost:${port}/api/auth/callback`;
    const display = document.getElementById('redirectUriDisplay');
    if (display) {
        display.textContent = redirectUri;
    }
}

function copyRedirectUri() {
    const display = document.getElementById('redirectUriDisplay');
    const text = display.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Redirect URI copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showAlert('Redirect URI copied to clipboard!', 'success');
    });
}

function checkUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const auth = urlParams.get('auth');
    
    if (auth === 'success') {
        showAlert('Authentication successful!', 'success');
        window.history.replaceState({}, document.title, '/');
        checkAuthStatus();
    } else if (auth === 'failed') {
        const error = urlParams.get('error');
        showAlert('Authentication failed: ' + (error || 'Unknown error'), 'error');
        window.history.replaceState({}, document.title, '/');
    }
}

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        
        if (data.authenticated) {
            document.getElementById('authStatus').textContent = 
                `Authenticated: ${data.accountEmail}`;
            document.getElementById('authStatus').classList.add('authenticated');
            document.getElementById('mainContent').style.display = 'block';
            document.getElementById('authSection').style.display = 'none';
            
            if (data.channels && data.channels.length > 0) {
                const select = document.getElementById('channelDropdown');
                select.innerHTML = '<option value="">-- Select Channel --</option>';
                data.channels.forEach(channel => {
                    const option = document.createElement('option');
                    option.value = channel.id;
                    option.textContent = `${channel.title} (${channel.subscribers} subscribers)`;
                    if (channel.id === data.selectedChannelId) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
                document.getElementById('channelSelect').style.display = 'block';
            }
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

async function uploadClientSecret() {
    const fileInput = document.getElementById('clientSecretFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('clientSecret', file);
    
    try {
        const response = await fetch('/api/auth/upload-client-secret', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Client secret uploaded successfully!', 'success');
            document.getElementById('loginBtn').disabled = false;
            clientSecretUploaded = true;
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error uploading client secret: ' + error.message, 'error');
    }
}

async function login() {
    try {
        if (!clientSecretUploaded) {
            showAlert('Please upload client_secret.json first before logging in.', 'error');
            return;
        }
        
        const response = await fetch('/api/auth/login');
        const data = await response.json();
        
        if (data.success) {
            showAlert('Redirecting to Google for authentication...', 'info');
            setTimeout(() => {
                window.location.href = data.authUrl;
            }, 1000);
        } else {
            let errorMsg = data.error;
            if (errorMsg.includes('OAuth2 client not initialized')) {
                errorMsg = 'Please upload client_secret.json file first.';
            }
            showAlert('Error: ' + errorMsg, 'error');
        }
    } catch (error) {
        showAlert('Error initiating login: ' + error.message, 'error');
    }
}

async function selectChannel() {
    const select = document.getElementById('channelDropdown');
    const channelId = select.value;
    
    if (!channelId) return;
    
    try {
        const response = await fetch('/api/auth/select-channel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ channelId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Channel selected successfully', 'success');
        }
    } catch (error) {
        showAlert('Error selecting channel: ' + error.message, 'error');
    }
}

async function parseExcel() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select an Excel file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('excelFile', file);
    
    try {
        const response = await fetch('/api/broadcasts/parse-excel', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            parsedBroadcasts = data.broadcasts;
            displayBroadcastPreview(data.broadcasts);
            showAlert(`Parsed ${data.broadcasts.length} broadcasts`, 'success');
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error parsing Excel: ' + error.message, 'error');
    }
}

function displayBroadcastPreview(broadcasts) {
    const preview = document.getElementById('broadcastPreview');
    const content = document.getElementById('previewContent');
    
    content.innerHTML = '';
    
    broadcasts.forEach((broadcast, index) => {
        const card = document.createElement('div');
        card.className = 'broadcast-card';
        card.innerHTML = `
            <h4>${index + 1}. ${broadcast.title}</h4>
            <p><strong>Description:</strong> ${broadcast.description.substring(0, 100)}...</p>
            <p><strong>Privacy:</strong> ${broadcast.privacyStatus}</p>
            <p><strong>Scheduled:</strong> ${new Date(broadcast.scheduledStartTime).toLocaleString()}</p>
        `;
        content.appendChild(card);
    });
    
    preview.style.display = 'block';
}

async function createBatchImmediate() {
    if (parsedBroadcasts.length === 0) {
        showAlert('No broadcasts to create', 'error');
        return;
    }
    
    const resultsDiv = document.getElementById('batchResults');
    resultsDiv.innerHTML = '<p>Creating broadcasts...</p>';
    
    try {
        const response = await fetch('/api/broadcasts/create-batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ broadcasts: parsedBroadcasts })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayBatchResults(data.results);
            showAlert(data.summary, 'success');
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error creating batch: ' + error.message, 'error');
    }
}

function displayBatchResults(results) {
    const resultsDiv = document.getElementById('batchResults');
    resultsDiv.innerHTML = '<h3>Results</h3>';
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = `result-item ${result.success ? 'success' : 'error'}`;
        item.innerHTML = `
            <strong>${result.title}</strong><br>
            ${result.success ? 
                `✓ Created - ID: ${result.broadcastId}` : 
                `✗ Failed - ${result.error}`}
        `;
        resultsDiv.appendChild(item);
    });
}

function showScheduleModal() {
    if (parsedBroadcasts.length === 0) {
        showAlert('No broadcasts to schedule', 'error');
        return;
    }
    
    const modal = document.getElementById('scheduleModal');
    modal.classList.add('show');
    
    const now = new Date();
    now.setHours(now.getHours() + 1);
    const datetime = now.toISOString().slice(0, 16);
    document.getElementById('batchScheduleTime').value = datetime;
}

function closeScheduleModal() {
    const modal = document.getElementById('scheduleModal');
    modal.classList.remove('show');
}

async function scheduleBatch() {
    const batchName = document.getElementById('batchName').value || 'Unnamed Batch';
    const scheduledTime = document.getElementById('batchScheduleTime').value;
    
    if (!scheduledTime) {
        showAlert('Please select a scheduled time', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/broadcasts/schedule-batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                broadcasts: parsedBroadcasts,
                scheduledTime,
                batchName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Batch scheduled successfully!', 'success');
            closeScheduleModal();
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error scheduling batch: ' + error.message, 'error');
    }
}

async function uploadVideo(schedule = false) {
    const videoFile = document.getElementById('videoFile').files[0];
    const thumbnailFile = document.getElementById('thumbnailFile').files[0];
    
    if (!videoFile) {
        showAlert('Please select a video file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('video', videoFile);
    if (thumbnailFile) formData.append('thumbnail', thumbnailFile);
    formData.append('title', document.getElementById('videoTitle').value || 'Untitled Video');
    formData.append('description', document.getElementById('videoDescription').value || '');
    formData.append('tags', document.getElementById('videoTags').value || '');
    formData.append('privacyStatus', document.getElementById('videoPrivacy').value);
    formData.append('madeForKids', document.getElementById('videoMadeForKids').checked);
    formData.append('containsSyntheticMedia', document.getElementById('videoSyntheticMedia').checked);
    formData.append('enableMonetization', document.getElementById('videoMonetization').checked);
    
    if (schedule) {
        const scheduledTime = prompt('Enter scheduled time (YYYY-MM-DD HH:MM):');
        if (!scheduledTime) return;
        formData.append('scheduledTime', new Date(scheduledTime).toISOString());
    }
    
    const endpoint = schedule ? '/api/videos/schedule-upload' : '/api/videos/upload';
    const progressDiv = document.getElementById('videoProgress');
    const progressBar = document.getElementById('videoProgressBar');
    
    try {
        progressDiv.style.display = 'block';
        progressBar.style.width = '0%';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        progressDiv.style.display = 'none';
        
        if (data.success) {
            showAlert(schedule ? 'Video upload scheduled!' : 'Video uploaded successfully!', 'success');
            document.getElementById('videoFile').value = '';
            document.getElementById('thumbnailFile').value = '';
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        progressDiv.style.display = 'none';
        showAlert('Error uploading video: ' + error.message, 'error');
    }
}

async function loadScheduledBatches() {
    try {
        const response = await fetch('/api/broadcasts/scheduled-batches');
        const data = await response.json();
        
        if (data.success) {
            displayScheduledBatches(data.batches);
        }
    } catch (error) {
        showAlert('Error loading scheduled batches: ' + error.message, 'error');
    }
}

function displayScheduledBatches(batches) {
    const list = document.getElementById('scheduledBatchesList');
    list.innerHTML = '';
    
    if (batches.length === 0) {
        list.innerHTML = '<p>No scheduled batches</p>';
        return;
    }
    
    batches.forEach(batch => {
        const card = document.createElement('div');
        card.className = 'broadcast-card';
        card.innerHTML = `
            <h4>${batch.name} <span class="status-badge ${batch.status}">${batch.status}</span></h4>
            <p><strong>Scheduled:</strong> ${new Date(batch.scheduledTime).toLocaleString()}</p>
            <p><strong>Broadcasts:</strong> ${batch.broadcasts.length}</p>
            ${batch.status === 'pending' ? 
                `<button onclick="cancelBatch('${batch.id}')" class="btn btn-danger">Cancel</button>` : 
                ''}
        `;
        list.appendChild(card);
    });
}

async function cancelBatch(batchId) {
    if (!confirm('Are you sure you want to cancel this batch?')) return;
    
    try {
        const response = await fetch(`/api/broadcasts/cancel-batch/${batchId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Batch cancelled', 'success');
            loadScheduledBatches();
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error cancelling batch: ' + error.message, 'error');
    }
}

async function clearCompletedBatches() {
    try {
        const response = await fetch('/api/broadcasts/clear-completed-batches', {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Completed batches cleared', 'success');
            loadScheduledBatches();
        }
    } catch (error) {
        showAlert('Error: ' + error.message, 'error');
    }
}

async function loadScheduledUploads() {
    try {
        const response = await fetch('/api/videos/scheduled-uploads');
        const data = await response.json();
        
        if (data.success) {
            displayScheduledUploads(data.uploads);
        }
    } catch (error) {
        showAlert('Error loading scheduled uploads: ' + error.message, 'error');
    }
}

function displayScheduledUploads(uploads) {
    const list = document.getElementById('scheduledUploadsList');
    list.innerHTML = '';
    
    if (uploads.length === 0) {
        list.innerHTML = '<p>No scheduled uploads</p>';
        return;
    }
    
    uploads.forEach((upload, index) => {
        const card = document.createElement('div');
        card.className = 'broadcast-card';
        card.innerHTML = `
            <h4>${upload.videoData.title} <span class="status-badge ${upload.status}">${upload.status}</span></h4>
            <p><strong>Scheduled:</strong> ${new Date(upload.scheduledTime).toLocaleString()}</p>
            ${upload.status === 'pending' ? 
                `<button onclick="cancelUpload(${index})" class="btn btn-danger">Cancel</button>` : 
                ''}
        `;
        list.appendChild(card);
    });
}

async function cancelUpload(index) {
    if (!confirm('Are you sure you want to cancel this upload?')) return;
    
    try {
        const response = await fetch(`/api/videos/cancel-upload/${index}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Upload cancelled', 'success');
            loadScheduledUploads();
        } else {
            showAlert('Failed to cancel upload', 'error');
        }
    } catch (error) {
        showAlert('Error: ' + error.message, 'error');
    }
}

async function clearCompletedUploads() {
    try {
        const response = await fetch('/api/videos/clear-completed-uploads', {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Completed uploads cleared', 'success');
            loadScheduledUploads();
        }
    } catch (error) {
        showAlert('Error: ' + error.message, 'error');
    }
}

async function loadUpcomingBroadcasts() {
    try {
        const response = await fetch('/api/broadcasts/upcoming');
        const data = await response.json();
        
        if (data.success) {
            displayUpcomingBroadcasts(data.broadcasts);
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error loading broadcasts: ' + error.message, 'error');
    }
}

function displayUpcomingBroadcasts(broadcasts) {
    const list = document.getElementById('upcomingBroadcastsList');
    list.innerHTML = '';
    
    if (broadcasts.length === 0) {
        list.innerHTML = '<p>No upcoming broadcasts</p>';
        return;
    }
    
    broadcasts.forEach(broadcast => {
        const card = document.createElement('div');
        card.className = 'broadcast-card';
        card.innerHTML = `
            <h4>${broadcast.snippet.title}</h4>
            <p><strong>Scheduled:</strong> ${new Date(broadcast.snippet.scheduledStartTime).toLocaleString()}</p>
            <p><strong>Privacy:</strong> ${broadcast.status.privacyStatus}</p>
            <p><strong>ID:</strong> ${broadcast.id}</p>
        `;
        list.appendChild(card);
    });
}

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName + 'Tab').classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'scheduled') {
        loadScheduledBatches();
        loadScheduledUploads();
    } else if (tabName === 'upcoming') {
        loadUpcomingBroadcasts();
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    document.querySelector('.container').insertBefore(
        alertDiv,
        document.querySelector('.container').firstChild.nextSibling
    );
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}
