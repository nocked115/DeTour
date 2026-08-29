"use client";

import { FormEvent, useMemo, useState } from "react";
import styles from "./page.module.css";

type Weather = "맑음" | "비";
type Activity = "산책" | "카페" | "구경";
type CrowdPreference = "조용한 곳" | "적당히 활기찬 곳" | "요즘 인기 있는 곳";

type PlannerInput = {
  currentLocation: string;
  destination: string;
  time: number;
  budget: number;
  weather: Weather;
  activity: Activity;
  crowdPreference: CrowdPreference;
};

type Recommendation = {
  name: string;
  duration: number;
  price: number;
  travelMinutes: number;
  crowd: CrowdPreference;
  reason: string;
};

const recommendationData: Record<Weather, Record<Activity, Recommendation[]>> = {
  맑음: {
    산책: [
      { name: "서울숲 산책", duration: 48, price: 0, travelMinutes: 8, crowd: "적당히 활기찬 곳", reason: "맑은 날, 이동과 산책을 합쳐도 여유 있게 다녀올 수 있어요." },
      { name: "한강 수변 산책", duration: 62, price: 0, travelMinutes: 12, crowd: "조용한 곳", reason: "사람이 비교적 적은 시간대라면 물가에서 잠깐 쉬기 좋아요." },
      { name: "골목 사진 산책", duration: 30, price: 0, travelMinutes: 6, crowd: "요즘 인기 있는 곳", reason: "짧은 시간에도 성수의 골목을 둘러볼 수 있어요." },
    ],
    카페: [
      { name: "성수 로스터리 카페", duration: 55, price: 7000, travelMinutes: 9, crowd: "적당히 활기찬 곳", reason: "목적지 방향에 있어 이동을 크게 돌아가지 않아요." },
      { name: "조용한 북카페", duration: 50, price: 8000, travelMinutes: 10, crowd: "조용한 곳", reason: "잠깐 앉아 쉬고 싶을 때 알맞은 차분한 선택지예요." },
      { name: "테이크아웃 카페", duration: 28, price: 5000, travelMinutes: 7, crowd: "요즘 인기 있는 곳", reason: "시간이 짧아도 커피 한 잔을 챙길 수 있어요." },
    ],
    구경: [
      { name: "독립서점", duration: 42, price: 0, travelMinutes: 8, crowd: "조용한 곳", reason: "가볍게 책과 문구를 둘러보기에 좋아요." },
      { name: "로컬 편집숍", duration: 50, price: 5000, travelMinutes: 11, crowd: "요즘 인기 있는 곳", reason: "새로운 브랜드를 발견하고 싶을 때 추천해요." },
      { name: "작은 전시 공간", duration: 58, price: 9000, travelMinutes: 12, crowd: "적당히 활기찬 곳", reason: "현재 시간 안에 전시 하나를 천천히 볼 수 있어요." },
    ],
  },
  비: {
    산책: [
      { name: "실내 식물원", duration: 52, price: 6000, travelMinutes: 10, crowd: "적당히 활기찬 곳", reason: "비를 피하면서도 천천히 걸을 수 있는 실내 공간이에요." },
      { name: "대형 서점 산책", duration: 45, price: 0, travelMinutes: 8, crowd: "조용한 곳", reason: "비 오는 날에도 실내에서 편하게 걷고 머무를 수 있어요." },
      { name: "복합문화공간", duration: 60, price: 0, travelMinutes: 12, crowd: "요즘 인기 있는 곳", reason: "전시와 상점을 한곳에서 둘러볼 수 있어요." },
    ],
    카페: [
      { name: "창가 카페", duration: 54, price: 8000, travelMinutes: 9, crowd: "적당히 활기찬 곳", reason: "비를 보며 쉬기에 좋은 가까운 실내 장소예요." },
      { name: "북카페", duration: 60, price: 9000, travelMinutes: 10, crowd: "조용한 곳", reason: "커피와 책을 함께 즐기며 비를 피할 수 있어요." },
      { name: "동네 베이커리", duration: 30, price: 6000, travelMinutes: 7, crowd: "요즘 인기 있는 곳", reason: "짧은 시간에도 따뜻한 음료와 빵을 즐길 수 있어요." },
    ],
    구경: [
      { name: "실내 전시 공간", duration: 55, price: 8000, travelMinutes: 10, crowd: "적당히 활기찬 곳", reason: "날씨 영향 없이 전시를 여유 있게 볼 수 있어요." },
      { name: "소품숍", duration: 32, price: 3000, travelMinutes: 8, crowd: "조용한 곳", reason: "비를 피하면서 짧게 둘러보기 좋은 실내 장소예요." },
      { name: "레코드숍", duration: 48, price: 0, travelMinutes: 11, crowd: "요즘 인기 있는 곳", reason: "새로운 음악을 발견하며 시간을 보내기 좋아요." },
    ],
  },
};

const crowdLabel: Record<CrowdPreference, string> = {
  "조용한 곳": "혼잡도 낮음 선호",
  "적당히 활기찬 곳": "적당한 활기 선호",
  "요즘 인기 있는 곳": "화제성 선호",
};

export default function DetourPlanner() {
  const [form, setForm] = useState<PlannerInput>({
    currentLocation: "서울숲역",
    destination: "성수역",
    time: 60,
    budget: 20000,
    weather: "맑음",
    activity: "카페",
    crowdPreference: "적당히 활기찬 곳",
  });
  const [submitted, setSubmitted] = useState<PlannerInput | null>(null);
  const [error, setError] = useState("");

  const recommendations = useMemo(() => {
    if (!submitted) return [];

    return recommendationData[submitted.weather][submitted.activity]
      .filter((place) => place.duration <= submitted.time && place.price <= submitted.budget)
      .sort((a, b) => Number(b.crowd === submitted.crowdPreference) - Number(a.crowd === submitted.crowdPreference));
  }, [submitted]);

  function updateField<Key extends keyof PlannerInput>(key: Key, value: PlannerInput[Key]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!form.currentLocation.trim() || !form.destination.trim()) {
      setError("현재 위치와 도착 위치를 모두 입력해 주세요.");
      setSubmitted(null);
      return;
    }

    if (form.budget <= 0) {
      setError("예산은 1원 이상으로 입력해 주세요.");
      setSubmitted(null);
      return;
    }

    setError("");
    setSubmitted(form);
  }

  return (
    <section className={styles.planner} id="planner" aria-labelledby="planner-title">
      <div className={styles.plannerHeader}>
        <div>
          <p className={styles.eyebrow}>MINI PREVIEW</p>
          <h2 id="planner-title">오늘의 빈칸을 채워볼까요?</h2>
        </div>
        <p>현재는 학습용 mock 데이터입니다. 다음 주에 주소를 실제 좌표와 경로 시간으로 바꿉니다.</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        <label className={styles.wideField}>
          현재 위치
          <input value={form.currentLocation} onChange={(event) => updateField("currentLocation", event.target.value)} placeholder="예: 서울숲역" />
        </label>
        <label className={styles.wideField}>
          도착 위치
          <input value={form.destination} onChange={(event) => updateField("destination", event.target.value)} placeholder="예: 성수역" />
        </label>
        <label className={styles.field}>
          남은 시간
          <select value={form.time} onChange={(event) => updateField("time", Number(event.target.value))}>
            <option value={30}>30분</option>
            <option value={60}>60분</option>
            <option value={90}>90분</option>
          </select>
        </label>
        <label className={styles.field}>
          예산
          <input type="number" min="1" step="1000" value={form.budget} onChange={(event) => updateField("budget", Number(event.target.value))} />
        </label>
        <label className={styles.field}>
          날씨
          <select value={form.weather} onChange={(event) => updateField("weather", event.target.value as Weather)}>
            <option value="맑음">☀️ 맑음</option>
            <option value="비">☔ 비 옴</option>
          </select>
        </label>
        <label className={styles.field}>
          하고 싶은 것
          <select value={form.activity} onChange={(event) => updateField("activity", event.target.value as Activity)}>
            <option value="산책">산책</option>
            <option value="카페">카페</option>
            <option value="구경">구경</option>
          </select>
        </label>
        <label className={styles.wideField}>
          지금 원하는 분위기
          <select value={form.crowdPreference} onChange={(event) => updateField("crowdPreference", event.target.value as CrowdPreference)}>
            <option value="조용한 곳">조용한 곳</option>
            <option value="적당히 활기찬 곳">적당히 활기찬 곳</option>
            <option value="요즘 인기 있는 곳">요즘 인기 있는 곳</option>
          </select>
        </label>
        {error ? <p className={styles.error} role="alert">{error}</p> : null}
        <button className={styles.submitButton} type="submit">작은 Detour 받아보기</button>

        {submitted ? (
          <div className={styles.result} aria-live="polite">
            <p className={styles.resultTitle}>{submitted.currentLocation}에서 {submitted.destination}로 가는 길, {submitted.activity}하고 싶다면</p>
            <p className={styles.resultNote}>{submitted.weather === "비" ? "비가 와서 실내 후보를 우선으로 골랐어요." : "맑은 날이라 야외 활동도 후보에 넣었어요."} {crowdLabel[submitted.crowdPreference]}를 먼저 보여드려요.</p>
            {recommendations.length ? (
              <div className={styles.recommendationList}>
                {recommendations.map((place, index) => (
                  <article className={styles.recommendationCard} key={place.name}>
                    <h3>TOP {index + 1}. {place.name}</h3>
                    <p className={styles.meta}>{place.duration}분 · {place.price.toLocaleString()}원 · {place.crowd}</p>
                    <p className={styles.reason}>{place.reason}</p>
                    <p className={styles.route}>{submitted.currentLocation}에서 예시 이동 {place.travelMinutes}분 · {submitted.destination} 방향</p>
                  </article>
                ))}
              </div>
            ) : <p className={styles.empty}>현재 조건에 맞는 후보가 없어요. 시간이나 예산을 조금 늘려 다시 시도해 보세요.</p>}
          </div>
        ) : null}
      </form>
    </section>
  );
}
