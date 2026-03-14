document.addEventListener('DOMContentLoaded', () => {
    const getIdeaBtn = document.getElementById('get-idea-btn');
    const completeBtn = document.getElementById('complete-btn');
    const ideaDisplay = document.getElementById('idea-display');
    const totalActsDisplay = document.getElementById('total-acts');
    const recentActsList = document.getElementById('recent-acts-list');

    let currentIdea = "";

    fetchStats();

    getIdeaBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/idea');
            const data = await response.json();
            currentIdea = data.idea;
            ideaDisplay.textContent = currentIdea;
            
            completeBtn.classList.remove('hidden');
            getIdeaBtn.textContent = "Get a Different Mission";
        } catch (error) {
            ideaDisplay.textContent = "Oops, our neighborhood network is busy. Try again!";
        }
    });

    completeBtn.addEventListener('click', async () => {
        if (!currentIdea) return;

        try {
            const response = await fetch('/api/acts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ act: currentIdea })
            });

            if (response.ok) {
                ideaDisplay.innerHTML = "<strong>Awesome job, neighbor!</strong> Ready for another?";
                completeBtn.classList.add('hidden');
                getIdeaBtn.textContent = "Get a Mission";
                currentIdea = "";
                
                fetchStats();
            }
        } catch (error) {
            alert("Couldn't record the act. But the community still appreciates it!");
        }
    });

    async function fetchStats() {
        try {
            const response = await fetch('/api/acts');
            const data = await response.json();
            
            totalActsDisplay.textContent = data.total;
            
            recentActsList.innerHTML = '';
            if (data.recent.length === 0) {
                recentActsList.innerHTML = '<li>Be the first to complete a mission today!</li>';
            } else {
                data.recent.forEach(record => {
                    const li = document.createElement('li');
                    li.textContent = record.act;
                    recentActsList.appendChild(li);
                });
            }
        } catch (error) {
            console.error("Error fetching stats:", error);
        }
    }
});
