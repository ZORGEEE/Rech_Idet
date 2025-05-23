document.addEventListener('DOMContentLoaded', function () {
    var infoModal = document.getElementById('infoModal');
    infoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var context = button.getAttribute('data-context');
        var roles = button.getAttribute('data-roles');
        var comment = button.getAttribute('data-comment');
        var text = button.getAttribute('data-text');

        document.getElementById('modal-context').textContent = context || '';
        document.getElementById('modal-roles').textContent = roles || '';
        document.getElementById('modal-text').innerHTML = text || '';

        if (comment && comment !== 'None') {
            document.getElementById('modal-comment').textContent = comment;
            document.getElementById('modal-comment-block').style.display = '';
        } else {
            document.getElementById('modal-comment-block').style.display = 'none';
        }
    });
});