import { CSSProperties, useContext, useEffect, useState } from "react";
import { AppContext } from "../components/AppContext";
import clsx from "clsx";
import colors from "../public/cta_data/theme.json";
import { useRouter } from "next/router";

import Header from "../components/header";
import HeartIcon from "../public/icons/heart.svg";
import CloseIcon from "../public/icons/close.svg";
import useFavorites, { Stop } from "../utils/useFavorites";
// import { setInterval } from "timers/promises";

type SongState = {
  wait_duration?: number;
  song_duration?: number;
  song_url?: string;
  favorite?: Stop;
  track_uri: string;
  time_left: number;
};

export default function Song() {
  const context = useContext(AppContext);
  const router = useRouter();
  const [state, setState] = useState<SongState>({
    time_left: NaN,
    track_uri: "1vUjqIGapgMyAFXOLUrYHO",
  });
  // const favorites = useFavorites(undefined);

  let style = {
    "--line": context.line ? colors[context.line] : colors["grey"],
  } as CSSProperties;

  // Hydrate data on load
  useEffect(() => {
    const fetchData = async () => {
      console.log("This went off");
      if (context.stop_id) {
        const data = await fetch(`/api/stop_id?stpid=${context.stop_id}`);
        const payload = await data.json();
        setState({
          ...state,
          song_url: payload["url"],
          song_duration: payload["track_duration"],
          wait_duration: payload["wait_duration"],
          time_left: payload["wait_duration"],
        });
      }
    };
    fetchData().catch(console.error);
  }, []);

  // Tick down timer; send back to home on timeout
  useEffect(() => {
    if (state.time_left < 2 && state.time_left !== NaN) {
      // Go home
      router.push("/");
    } else {
      const intervalId = setInterval(() => {
        setState({ ...state, time_left: state.time_left - 1 });
      }, 1000);
      return () => clearInterval(intervalId);
    }
  }, [state.time_left]);

  // Make delete button work
  useEffect(() => {
    if (!context.stop_id) {
      // Force back to home
      router.push("/");
    }
  }, [context.stop_id]);

  return (
    <div style={style} className={"bg-[color:var(--line)] min-h-screen"}>
      <div className="max-w-screen-sm w-full mx-auto">
        <Header />
        <div className="border-t-2 border-white pt-6">
          <h1
            className={clsx(
              "text-center text-white tracking-tighter font-bold",
              context.stop_name && context.stop_name.split(" ").length > 2
                ? "text-4xl"
                : "text-5xl"
            )}
          >
            {context.stop_name ? context.stop_name : "Aieee"}
          </h1>
          <div className="flex min-w-full my-4 px-6">
            <button
              onClick={() => {
                context.updateAppContext
                  ? context.updateAppContext({
                      ...context,
                      stop_id: undefined,
                      line: undefined,
                      stop_name: undefined,
                      bound_for: undefined,
                    })
                  : {};
              }}
            >
              <CloseIcon />
            </button>
            <p className="text-center w-full text-white tracking-tight text-xl">
              {context.bound_for ? `To ${context.bound_for}` : "Aieee"}
            </p>
            <button onClick={() => {}} className="ml-auto">
              <HeartIcon />
            </button>
          </div>
        </div>
        <div className="border-t-2 border-white flex-col flex">
          <iframe
            src={`https://open.spotify.com/embed/track/${state.track_uri}?utm_source=generator&theme=0`}
            width="100%"
            height="80"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
          ></iframe>
        </div>
        <h2 className="text-center tracking-tight text-2xl text-white border-t-2 border-white py-4">
          <span className="font-bold">
            {state.wait_duration
              ? `Inbound in ${Math.ceil(state.time_left / 60)} mins`
              : "No network connection"}
          </span>
        </h2>
      </div>
    </div>
  );
}
