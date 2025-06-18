import React, { useState } from 'react';

const Prerequisites = ({ onNext, onPrev }) => {
  const [checkedItems, setCheckedItems] = useState({});

  const handleCheckboxChange = (id) => {
    setCheckedItems(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const requirements = [
    {
      id: 'os',
      category: 'Operating System',
      icon: 'fas fa-desktop',
      items: [
        { id: 'ubuntu', text: 'Ubuntu 20.04 LTS or later', required: true },
        { id: 'memory', text: '8GB RAM minimum, 16GB recommended', required: true },
        { id: 'storage', text: '50GB available disk space', required: true }
      ]
    },
    {
      id: 'software',
      category: 'Software Dependencies',
      icon: 'fas fa-code',
      items: [
        { id: 'python', text: 'Python 3.8 or later', required: true },
        { id: 'docker', text: 'Docker Engine 20.10+', required: true },
        { id: 'git', text: 'Git version control', required: true },
        { id: 'nodejs', text: 'Node.js 16+ (for web interface)', required: false }
      ]
    },
    {
      id: 'hardware',
      category: 'Hardware Requirements',
      icon: 'fas fa-microchip',
      items: [
        { id: 'gpu', text: 'NVIDIA GPU with CUDA support (recommended)', required: false },
        { id: 'usb', text: 'USB 3.0 ports for drone connection', required: true },
        { id: 'network', text: 'Stable internet connection', required: true }
      ]
    }
  ];

  const getTotalRequiredItems = () => {
    return requirements.reduce((total, category) => 
      total + category.items.filter(item => item.required).length, 0
    );
  };

  const getCheckedRequiredItems = () => {
    return requirements.reduce((total, category) => 
      total + category.items.filter(item => item.required && checkedItems[item.id]).length, 0
    );
  };

  const canProceed = getCheckedRequiredItems() === getTotalRequiredItems();

  return (
    <div className="content-section prerequisites-section">
      <div className="content-header">
        <div className="step-indicator">
          <span className="step-number">02</span>
          <span className="step-label">Prerequisites</span>
        </div>
        <h2 className="content-title">System Requirements</h2>
        <p className="content-subtitle">
          Ensure your system meets these requirements before installation
        </p>
      </div>

      <div className="content-body">
        <div className="requirements-checklist">
          {requirements.map(category => (
            <div key={category.id} className="requirement-category">
              <div className="category-header">
                <i className={category.icon}></i>
                <h3>{category.category}</h3>
              </div>
              
              <div className="category-items">
                {category.items.map(item => (
                  <div key={item.id} className="requirement-item">
                    <label className="requirement-checkbox">
                      <input
                        type="checkbox"
                        checked={checkedItems[item.id] || false}
                        onChange={() => handleCheckboxChange(item.id)}
                      />
                      <span className="checkmark"></span>
                      <span className="requirement-text">
                        {item.text}
                        {item.required && <span className="required-badge">Required</span>}
                      </span>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="verification-panel">
          <h3>Quick System Check</h3>
          <p>Run these commands to verify your system:</p>
          
          <div className="code-blocks">
            <div className="code-block">
              <div className="code-header">
                <span>Check Python Version</span>
                <button className="copy-btn">
                  <i className="fas fa-copy"></i>
                </button>
              </div>
              <code>python3 --version</code>
            </div>
            
            <div className="code-block">
              <div className="code-header">
                <span>Check Docker Installation</span>
                <button className="copy-btn">
                  <i className="fas fa-copy"></i>
                </button>
              </div>
              <code>docker --version && docker compose version</code>
            </div>
            
            <div className="code-block">
              <div className="code-header">
                <span>Check Available Memory</span>
                <button className="copy-btn">
                  <i className="fas fa-copy"></i>
                </button>
              </div>
              <code>free -h</code>
            </div>
          </div>
        </div>

        <div className="installation-options">
          <h3>Choose Your Installation Path</h3>
          <div className="options-grid">
            <div className="option-card">
              <h4>Standard Installation</h4>
              <p>Perfect for single-machine setups and local development</p>
              <ul>
                <li>Local deployment</li>
                <li>Single user access</li>
                <li>Simplified configuration</li>
              </ul>
            </div>
            <div className="option-card">
              <h4>Cloud2Edge Installation</h4>
              <p>Advanced setup for distributed computing and cloud integration</p>
              <ul>
                <li>Multi-node deployment</li>
                <li>Cloud connectivity</li>
                <li>Scalable architecture</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="navigation-buttons">
          <button className="btn btn-prev" onClick={onPrev}>
            <i className="fas fa-arrow-left"></i>
            <span>Previous: Motivation</span>
          </button>
          
          <div className="requirements-status">
            <div className="status-indicator">
              <span className="status-count">
                {getCheckedRequiredItems()} / {getTotalRequiredItems()}
              </span>
              <span className="status-label">Required items completed</span>
            </div>
          </div>
          
          <button 
            className={`btn btn-next ${!canProceed ? 'disabled' : ''}`} 
            onClick={onNext}
            disabled={!canProceed}
          >
            <span>Next: Installation</span>
            <i className="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>

      <div className="progress-indicator">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: '50%'}}></div>
        </div>
        <span className="progress-text">Step 2 of 4</span>
      </div>
    </div>
  );
};

export default Prerequisites;