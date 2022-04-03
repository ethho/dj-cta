import { CSSProperties } from "react";
import clsx from "clsx";
import colors from "../public/cta_data/theme.json";
import { Stop } from "../utils/useFavorites";

const StopSign: React.FC<{ stop: Stop; onClick: (stop: Stop) => void }> = ({
  stop,
  onClick,
}) => {
  let style = {
    "--currLine": stop.line ? colors[stop.line] : colors["grey"],
  } as CSSProperties;
  return (
    <button
      className="flex items-center bg-grey w-full mb-2"
      onClick={() => onClick(stop)}
    >
      <div
        style={style}
        className={clsx("w-6 h-16", "bg-[color:var(--currLine)]")}
      ></div>
      <h2 className="font-bold mx-6 tracking-tighter text-2xl">
        {stop.stop_name}
      </h2>
      <p className="ml-auto mr-6">
        {stop.distance ? stop.distance.toFixed(2) : "?"} mi
      </p>
      <div
        style={style}
        className={clsx("w-6 h-16", "bg-[color:var(--currLine)]")}
      ></div>
    </button>
  );
};

export default StopSign;
