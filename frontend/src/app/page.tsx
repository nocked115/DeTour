import DetourPlanner from "./detour-planner";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.page}>
      <nav className={styles.nav} aria-label="주요 메뉴">
        <a className={styles.logo} href="#top" aria-label="DETOUR 홈">
          detour<span>.</span>
        </a>
        <p>Shortest isn&apos;t always best.</p>
      </nav>

      <section className={styles.hero} id="top">
        <p className={styles.eyebrow}>YOUR SPARE TIME, YOUR LITTLE ROUTE</p>
        <h1>
          30분 남았어?
          <br />
          <mark>그냥 보내지 마.</mark>
        </h1>
        <p className={styles.intro}>
          목적지에 바로 가기엔 아쉽고, 뭘 하기엔 애매한 시간.
          <br />
          DETOUR가 지금의 조건에 맞는 작은 우회로를 골라드려요.
        </p>
        <a className={styles.heroCta} href="#planner">
          내 Detour 찾기 →
        </a>
      </section>

      <section className={styles.featureList} aria-label="DETOUR 추천 기준">
        <article>
          <span>01 · TIME FIT</span>
          <h2>시간 안에 딱</h2>
          <p>현재 위치에서 들렀다가 목적지에 도착할 수 있는지 먼저 확인해요.</p>
        </article>
        <article>
          <span>02 · CONTEXT FIT</span>
          <h2>날씨와 분위기까지</h2>
          <p>비 오는 날엔 실내를, 조용히 쉬고 싶다면 덜 붐비는 곳을 우선해요.</p>
        </article>
        <article>
          <span>03 · CLEAR REASON</span>
          <h2>이유까지 분명하게</h2>
          <p>시간·비용·혼잡도를 함께 보여줘서 직접 납득하고 선택할 수 있어요.</p>
        </article>
      </section>

      <DetourPlanner />

      <footer className={styles.footer}>
        <span>DETOUR © 2026</span>
        <span>가장 빠른 길이 아니라, 나에게 맞는 길.</span>
      </footer>
    </main>
  );
}
