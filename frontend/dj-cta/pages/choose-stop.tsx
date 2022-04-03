import { useContext, useEffect, useState } from "react";
import { Stop } from "../utils/useFavorites";
import StopSign from "../components/stop-sign";

// Cmponents
import {
  LineColorsType,
  AppContext,
  AppContextType,
} from "../components/AppContext";
import Container from "../components/container";
import Header from "../components/header";
import FWLink from "../components/fw-link";
import LineSelect from "../components/line-select";
import StopSelect from "../components/stop-select";

// Assets
import clsx from "clsx";
import CircleArrow from "../public/icons/circle-arrow.svg";
import l_stops from "../public/l-stops.json";
import cta_routes from "../public/cta_data/routes.json";

const SectionBox: React.FC<{ title: string }> = ({ children, title }) => (
  <div className="bg-grey my-2 pt-4">
    <h2 className="text-4xl tracking-tighter font-bold px-6 pb-4">{title}</h2>
    {children}
  </div>
);

const ChooseStop = () => {
  const context: AppContextType = useContext(AppContext);
  type Dir = "N" | "S" | "E" | "W" | undefined;
  type ChooseStopState = {
    dir?: Dir;
    stops?: Stop[];
    geo_status: string;
  };

  const [state, setState] = useState<ChooseStopState>({
    geo_status: "Enable location access to find stops near you",
  });

  function getLine(stop: string) {
    let line = l_stops.filter((l) => l.STATION_NAME == stop)[0];
    if (line) {
      let foo = Object.entries(line).filter(([k, v]) => v === true);
      if (foo) {
        return foo[0][0].toLowerCase();
      } else {
        return undefined;
      }
    } else {
      return undefined;
    }
  }

  useEffect(() => {
    const getData = async () => {
      try {
        if (!navigator.geolocation) {
          setState({
            ...state,
            geo_status: "Geolocation is not supported by your browser",
          });
        } else {
          setState({ ...state, geo_status: "Locating..." });
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              let res = await fetch(
                `/api/get_nearby_stops?lon=${position.coords.latitude}&lat=${position.coords.longitude}`
              );
              let json = await res.json();
              if (json.detail == "Not Found") {
                setState({
                  ...state,
                  geo_status: "Can't retrieve your location",
                });
              } else {
                console.log(json.stops);
                if (json.stops) {
                  try {
                    console.log("Got here!");
                    let new_stops = json.stops.map(
                      (s: {
                        stop_id: number;
                        stop_name: string;
                        miles_away: number;
                      }) => ({
                        stop_id: s.stop_id,
                        stop_name: s.stop_name,
                        distance: s.miles_away,
                        line: getLine(s.stop_name),
                      })
                    );
                    console.log(new_stops);
                    setState({
                      ...state,
                      stops: new_stops,
                      geo_status: "Here are the nearest stations to you:",
                    });
                  } catch {
                    setState({
                      ...state,
                      geo_status: "Could not parse stops",
                    });
                  }
                }
              }
            },
            () => {
              setState({
                ...state,
                geo_status: "Can't retrieve your location",
              });
            }
          );
        }
      } catch {}
    };
    getData().catch(console.error);
  }, []);

  return (
    <Container>
      <Header />
      <h1 className="text-5xl tracking-tighter font-bold mx-6 my-8">
        Pick your stop
      </h1>
      <div className="px-6 mt-6">
        <h2 className="tracking-tighter font-bold text-3xl pt-3 border-t-2 dark:border-white">
          Stops near you
        </h2>
        <p className="tracking-tight my-4">{state.geo_status}</p>
      </div>
      {state.stops
        ?.filter((s) => s.line)
        .slice(0, 5)
        .map((s, k) => (
          <StopSign
            key={k}
            stop={s}
            onClick={(s) =>
              context.updateAppContext
                ? context.updateAppContext({
                    ...context,
                    stop_id: s.stop_id,
                    line: s.line,
                    stop_name: s.stop_name,
                  })
                : {}
            }
          />
        ))}
      <div className="px-6 mt-6">
        <h2 className="mb-4 tracking-tighter font-bold text-3xl pt-3 border-t-2 dark:border-white">
          Choose stop manually
        </h2>
      </div>
      <SectionBox title="Line">
        <LineSelect />
      </SectionBox>
      <SectionBox title="Stop">
        <StopSelect />
      </SectionBox>
      <SectionBox title="Direction">
        <div className="grid grid-cols-2 w-auto border-black border-t-8">
          <button
            className={clsx(
              "pl-6 py-2 border-r-8 border-black text-left text-xl tracking-tight font-bold",
              "hover:bg-white hover:text-black"
            )}
            onClick={() =>
              context.updateAppContext && context.stop_name && context.line
                ? context.updateAppContext({
                    ...context,
                    stop_id: l_stops.filter(
                      (s) =>
                        s.STATION_NAME == context.stop_name &&
                        (s.DIRECTION_ID == "W" || s.DIRECTION_ID == "N")
                    )[0].STOP_ID,
                    bound_for: cta_routes[context.line]?.at(0),
                  })
                : {}
            }
          >
            <CircleArrow className="w-6 h-6 rotate-180 inline mr-2" />
            {context.stop_name && context.line
              ? `To ${cta_routes[context.line]?.at(0)}`
              : "Choose a stop"}
          </button>
          <button
            className="text-right pr-6 text-xl tracking-tight font-bold hover:bg-white hover:text-black"
            onClick={() =>
              context.updateAppContext && context.stop_name && context.line
                ? context.updateAppContext({
                    ...context,
                    stop_id: l_stops.filter(
                      (s) =>
                        s.STATION_NAME == context.stop_name &&
                        (s.DIRECTION_ID == "E" || s.DIRECTION_ID == "S")
                    )[0].STOP_ID,
                    bound_for: cta_routes[context.line]?.at(-1),
                  })
                : {}
            }
          >
            {context.line && context.stop_name
              ? `To ${cta_routes[context.line].at(-1)}`
              : "Choose a stop"}
            <CircleArrow className="w-6 h-6 inline ml-2" />
          </button>
        </div>
      </SectionBox>
      <FWLink
        text={context.stop_id ? `Find a song!` : "Almost done..."}
        size="small"
        bgColor={context.line}
        href="/song"
        disabled={!context.stop_id}
      />
    </Container>
  );
};

export default ChooseStop;
