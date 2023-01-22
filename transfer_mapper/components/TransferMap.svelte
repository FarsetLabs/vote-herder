<script>
  import { scaleLinear } from "d3-scale";

  const stageone = [
    { candidate: "Tony", votes: 6000 },
    { candidate: "Barbara", votes: 2000 },
    { candidate: "Susan", votes: 4000 },
  ];

  const quota = 5000;

  const yTicks = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000];
  const padding = { top: 20, right: 15, bottom: 20, left: 25 };

  let width = 500;
  let height = 200;

  function formatMobile(tick) {
    return "'" + tick.toString().slice(-2);
  }

  $: xScale = scaleLinear()
    .domain([0, stageone.length])
    .range([padding.left, width - padding.right]);

  $: yScale = scaleLinear()
    .domain([0, Math.max.apply(null, yTicks)])
    .range([height - padding.bottom, padding.top]);

  $: innerWidth = width - (padding.left + padding.right);
  $: barWidth = innerWidth / stageone.length;
</script>

<h2>US birthrate by candidate</h2>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
  <svg>
    <!-- y axis -->
    <g class="axis y-axis">
      {#each yTicks as tick}
        <g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
          <line x2="100%" />
          <text y="-4">{tick} {tick === 20 ? " per 1,000 population" : ""}</text
          >
        </g>
      {/each}
    </g>

    <!-- x axis -->
    <g class="axis x-axis">
      {#each stageone as point, i}
        <g class="tick" transform="translate({xScale(i)},{height})">
          <text x={barWidth / 2} y="-4"
            >{width > 380
              ? point.candidate
              : formatMobile(point.candidate)}</text
          >
        </g>
      {/each}
    </g>

    <g class="bars">
      {#each stageone as point, i}
        <rect
          x={xScale(i) + 2}
          y={yScale(point.votes)}
          width={barWidth - 4}
          height={yScale(0) - yScale(point.votes)}
        />
      {/each}
    </g>

    <!-- quota line -->
    <g>
      <line class="quota-line"
        x1={padding.left}
        y1={yScale(quota)}
        x2={width + padding.right}
        y2={yScale(quota)}
        stroke="black"
        stroke-dasharray="2"
      />
    </g>
  </svg>
</div>

<style>
  h2 {
    text-align: center;
  }

  .chart {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  svg {
    position: relative;
    width: 100%;
    height: 200px;
  }

  .tick {
    font-family: Helvetica, Arial;
    font-size: 0.725em;
    font-weight: 200;
  }

  .quota-line {
    stroke: rgb(233, 7, 7);
    stroke-width: 2;
    stroke-dasharray: 10;
    opacity: 0.5;

  }

  .tick line {
    stroke: #e2e2e2;
    stroke-dasharray: 2;
  }

  .tick text {
    fill: #ccc;
    text-anchor: start;
  }

  .tick.tick-0 line {
    stroke-dasharray: 0;
  }

  .x-axis .tick text {
    text-anchor: middle;
  }

  .bars rect {
    fill: #a11;
    stroke: none;
    opacity: 0.65;
  }
</style>
