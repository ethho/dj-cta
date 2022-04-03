import { useContext } from "react";

import { AppContext, AppContextType } from "../components/AppContext";
import Container from "../components/container";
import Header from "../components/header";
import FWLink from "../components/fw-link";
import clsx from "clsx";
import TrainIcon from "../public/icons/train.svg";
// import l_stops from "../public/l_stops.json";
import cta_routes from "../public/cta_data/routes.json";

const SectionBox: React.FC<{ title: string }> = ({ children, title }) => (
  <div className="bg-grey my-2 py-4">
    <h2 className="text-4xl tracking-tighter font-bold px-6">{title}</h2>
    {children}
  </div>
);

const ChooseStop = () => {
  const state: AppContextType = useContext(AppContext);

  type LBProps = { bgColor: string };
  const LineBox = (props: LBProps) => (
    <div
      className={clsx(
        "w-16 h-16 flex items-center mt-4",
        props.bgColor,
        state.line == props.bgColor.slice(5)
          ? "border-4 border-white"
          : "border-none"
      )}
      onClick={() =>
        state.setContext({ ...state, line: props.bgColor.slice(5) })
      }
    >
      {state.line == props.bgColor.slice(5) && (
        <TrainIcon className="mx-auto" />
      )}
    </div>
  );

  return (
    <Container>
      <Header />
      <h1 className="text-5xl tracking-tighter font-bold mx-6 my-12">
        Pick your stop
      </h1>
      <SectionBox title="Line">
        <div className="flex overflow-scroll">
          <LineBox bgColor="bg-red" />
          <LineBox bgColor="bg-blue" />
          <LineBox bgColor="bg-brown" />
          <LineBox bgColor="bg-green" />
          <LineBox bgColor="bg-orange" />
          <LineBox bgColor="bg-pink" />
          <LineBox bgColor="bg-purple" />
          <LineBox bgColor="bg-yellow" />
        </div>
      </SectionBox>
      <SectionBox title="Stop">
        <div className="mx-6">
          {state.line &&
            cta_routes[state.line.toUpperCase()].map((s, k) => (
              <p key={k}>{s}</p>
            ))}
        </div>
      </SectionBox>
      <SectionBox title="Direction">
        <div className="flex divide-x w-auto">
          <button className="min-w-auto">North</button>
          <button>South</button>
        </div>
      </SectionBox>
      <FWLink text="Done" size="small" bgColor="bg-red" href="/song" />
    </Container>
  );
};

export default ChooseStop;
