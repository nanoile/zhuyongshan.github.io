const search = document.querySelector('#post-search');
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const posts = [...document.querySelectorAll('[data-post]')];
const count = document.querySelector('#post-count');
const emptyState = document.querySelector('#no-posts');
let category = 'All';

function updatePosts() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  posts.forEach(post => {
    const matchesCategory = category === 'All' || category === post.dataset.category;
    const matchesSearch = post.dataset.search.toLocaleLowerCase().includes(query);
    post.hidden = !(matchesCategory && matchesSearch);
    if (!post.hidden) visible++;
  });
  filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  count.textContent = `${visible} ${visible === 1 ? 'post' : 'posts'}${query ? ' found' : ''}`;
  emptyState.hidden = visible !== 0;
}
filterButtons.forEach(button => button.addEventListener('click', () => {
  category = button.dataset.filter;
  updatePosts();
}));
search.addEventListener('input', updatePosts);
document.querySelector('#reset-search').addEventListener('click', () => {
  category = 'All';
  search.value = '';
  updatePosts();
  search.focus();
});
updatePosts();
