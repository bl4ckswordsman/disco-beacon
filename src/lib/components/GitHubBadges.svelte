<script lang="ts">
    export let owner: string;
    export let repo: string;

    const visitsUrl = `https://badges.pufler.dev/visits/${owner}/${repo}`;
    const hitsUrl = `https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2F${owner}%2F${repo}&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Daily+hits&edge_flat=false`;
</script>

<div>
    <a href={`https://github.com/${owner}`}>
        <img src={visitsUrl} alt="Visits Badge"/>
    </a>
    <a href={`https://hits.seeyoufarm.com/api/count/graph/dailyhits.svg?url=https://github.com/${owner}/${repo}`}>
        <img src={hitsUrl} alt="Hits Badge"/>
    </a>
</div>

<style>
    div {
        display: flex;
        gap: 10px;
    }
</style>