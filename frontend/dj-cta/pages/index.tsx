import Container from "../components/container";
import Header from "../components/header";
import FWLink from "../components/fw-link";

export default function Home() {
  return (
    <Container>
      <Header />
      <div>
        <div className="px-6 mb-8">
          <h1 className="text-6xl font-bold tracking-tighter py-6">DJ CTA</h1>
          <p className="tracking-tight text-xl">
            Play a random song from your Spotify library before your train
            arrives
          </p>
        </div>
      </div>
      <FWLink text="Choose your stop" href="/choose-stop" size="large" />
      <div className="px-6 mt-6 ">
        <h2 className="tracking-tighter font-bold text-3xl pt-3 border-t-2 dark:border-white">
          Install this site as a PWA
        </h2>
        <p className="tracking-tight text-xl mt-4">
          Use this site like an app! See{" "}
          <a
            href="https://mobilesyrup.com/2020/05/24/how-install-progressive-web-app-pwa-android-ios-pc-mac/"
            className="text-blue hover:underline"
          >
            this guide
          </a>{" "}
          to install.
        </p>
      </div>
    </Container>
  );
}
