// Main JavaScript functionality
class EdunexaApp {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeComponents();
    }
    
    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuButton = document.querySelector('[data-mobile-menu-toggle]');
        const mobileMenu = document.querySelector('[data-mobile-menu]');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }
        
        // Flash message auto-hide
        this.autoHideFlashMessages();
        
        // Form submissions
        this.setupFormHandlers();
    }
    
    initializeComponents() {
        // Initialize tooltips, modals, etc.
        this.initializeTooltips();
        this.initializeModals();
    }
    
    autoHideFlashMessages() {
        const flashMessages = document.querySelectorAll('[data-flash-message]');
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }, 5000);
        });
    }
    
    setupFormHandlers() {
        // Setup AJAX form submissions
        const ajaxForms = document.querySelectorAll('[data-ajax-form]');
        ajaxForms.forEach(form => {
            form.addEventListener('submit', this.handleAjaxForm.bind(this));
        });
    }
    
    async handleAjaxForm(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const submitButton = form.querySelector('[type="submit"]');
        
        // Show loading state
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Processing...';
        submitButton.disabled = true;
        
        try {
            const response = await fetch(form.action, {
                method: form.method || 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification('Success!', result.message || 'Operation completed successfully', 'success');
                if (result.redirect) {
                    window.location.href = result.redirect;
                }
            } else {
                this.showNotification('Error', result.error || 'An error occurred', 'error');
            }
        } catch (error) {
            this.showNotification('Error', 'Network error occurred', 'error');
        } finally {
            // Restore button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    }
    
    showNotification(title, message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 z-50 transform transition-all duration-300 ${
            type === 'success' ? 'border-l-4 border-green-400' :
            type === 'error' ? 'border-l-4 border-red-400' :
            'border-l-4 border-blue-400'
        }`;
        
        notification.innerHTML = `
            <div class="p-4">
                <div class="flex items-start">
                    <div class="ml-3 w-0 flex-1">
                        <p class="text-sm font-medium text-gray-900">${title}</p>
                        <p class="mt-1 text-sm text-gray-500">${message}</p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex">
                        <button class="inline-flex text-gray-400 hover:text-gray-500" onclick="this.parentElement.parentElement.parentElement.parentElement.remove()">
                            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    initializeTooltips() {
        // Simple tooltip implementation
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip.bind(this));
            element.addEventListener('mouseleave', this.hideTooltip.bind(this));
        });
    }
    
    showTooltip(event) {
        const element = event.target;
        const tooltipText = element.getAttribute('data-tooltip');
        
        const tooltip = document.createElement('div');
        tooltip.className = 'absolute bg-gray-900 text-white text-xs rounded py-1 px-2 z-50';
        tooltip.textContent = tooltipText;
        tooltip.id = 'tooltip';
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    }
    
    hideTooltip() {
        const tooltip = document.getElementById('tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
    
    initializeModals() {
        // Modal functionality
        const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', this.openModal.bind(this));
        });
        
        const modalCloses = document.querySelectorAll('[data-modal-close]');
        modalCloses.forEach(close => {
            close.addEventListener('click', this.closeModal.bind(this));
        });
    }
    
    openModal(event) {
        const trigger = event.target;
        const modalId = trigger.getAttribute('data-modal-trigger');
        const modal = document.getElementById(modalId);
        
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }
    
    closeModal(event) {
        const close = event.target;
        const modal = close.closest('[data-modal]');
        
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EdunexaApp();
});

// Utility functions
window.EdunexaUtils = {
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    formatDuration: function(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    },
    
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }
};