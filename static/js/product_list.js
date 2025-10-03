/* Product List JavaScript */

function getCsrfToken() {
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
}

function escapeHtml(value) {
    if (typeof value !== 'string') {
        return value;
    }
    return value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

let productToDelete = null;

function toggleView(view) {
    const tableView = document.getElementById('tableViewContent');
    const gridView = document.getElementById('gridViewContent');
    const tableBtn = document.getElementById('tableView');
    const gridBtn = document.getElementById('gridView');

    if (view === 'table') {
        tableView.classList.remove('d-none');
        gridView.classList.add('d-none');
        tableBtn.classList.add('active');
        gridBtn.classList.remove('active');
        localStorage.setItem('productView', 'table');
    } else {
        tableView.classList.add('d-none');
        gridView.classList.remove('d-none');
        gridBtn.classList.add('active');
        tableBtn.classList.remove('active');
        localStorage.setItem('productView', 'grid');
    }
}

function deleteProduct(id, name) {
    productToDelete = id;
    const safeName = escapeHtml(name);
    document.getElementById('productName').textContent = name;
    
    // Reset the modal to basic delete confirmation
    document.getElementById('deleteModalBody').innerHTML = `
        <p>Are you sure you want to delete the product <strong>${safeName}</strong>?</p>
        <p class="text-muted">This action cannot be undone.</p>
    `;
    
    document.getElementById('confirmDelete').innerHTML = `
        <i class="fas fa-trash"></i> Delete Product
    `;
    document.getElementById('confirmDelete').className = 'btn btn-danger';
    
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

function exportToExcel() {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category') || '';
    const search = urlParams.get('search') || '';
    
    let exportUrl = window.exportProductsUrl; // This will be set in the template
    const params = new URLSearchParams();
    
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    
    if (params.toString()) {
        exportUrl += '?' + params.toString();
    }
    
    window.location.href = exportUrl;
}

// Handle delete confirmation
function handleDeleteConfirmation() {
    if (!productToDelete) return;
    
    const formData = new FormData();
    const forceDelete = document.getElementById('confirmDelete').dataset.forceDelete === 'true';
    const csrfToken = getCsrfToken();
    
    if (forceDelete) {
        formData.append('force_delete', 'true');
    }
    if (csrfToken) {
        formData.append('csrf_token', csrfToken);
    }
    
    // Show loading state
    const button = document.getElementById('confirmDelete');
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Deleting...';
    button.disabled = true;
    
    fetch(`/product/delete/${productToDelete}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Success - reload page to show updated list and flash message
            window.location.reload();
        } else if (data.has_movements) {
            // Product has movements, ask for confirmation
            showForceDeleteConfirmation(data);
        } else {
            // Other error
            alert('Error: ' + data.message);
            resetDeleteButton(button, originalText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the product');
        resetDeleteButton(button, originalText);
    });
}

function showForceDeleteConfirmation(data) {
    // Update modal content for force delete confirmation
    const safeName = escapeHtml(data.product_name);
    const safeMessage = escapeHtml(data.message);
    document.getElementById('deleteModalBody').innerHTML = `
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Warning!</strong> ${safeMessage}
        </div>
        <p><strong>This will permanently delete:</strong></p>
        <ul>
            <li>The product: <strong>${safeName}</strong></li>
            <li>All <strong>${data.movement_count}</strong> stock movements</li>
        </ul>
        <p class="text-danger"><strong>This action cannot be undone!</strong></p>
    `;
    
    const button = document.getElementById('confirmDelete');
    button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Yes, Delete Everything';
    button.className = 'btn btn-danger';
    button.dataset.forceDelete = 'true';
    button.disabled = false;
}

function resetDeleteButton(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
    button.dataset.forceDelete = 'false';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize view based on localStorage
    const savedView = localStorage.getItem('productView') || 'table';
    toggleView(savedView);
    
    // Set up delete confirmation handler
    document.getElementById('confirmDelete').addEventListener('click', handleDeleteConfirmation);
    
    // Auto-submit form on category change
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
    
    // Handle modal close - reset state
    document.getElementById('deleteModal').addEventListener('hidden.bs.modal', function() {
        productToDelete = null;
        const button = document.getElementById('confirmDelete');
        button.dataset.forceDelete = 'false';
        button.disabled = false;
    });
});