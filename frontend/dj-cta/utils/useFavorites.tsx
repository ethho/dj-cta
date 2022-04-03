import { useEffect, useState } from "react";
import { LineColorsType } from "../components/AppContext";

export type Stop = {
  line?: LineColorsType;
  stop_name?: string;
  stop_id?: number;
  bound_for?: string;
};

export default function useFavorites(stop: Stop | undefined) {
  const [favorites, setFavorites] = useState<Stop[]>([]);

  // Hydrate existing on startup
  useEffect(() => {
    let raw_favs = localStorage.getItem("favs");
    if (raw_favs) {
      let favs: Stop[] = JSON.parse(raw_favs);
      setFavorites(favs);
    }
  }, []);

  // Add favorite to storage
  useEffect(() => {
    if (stop) {
      // Remove duplicates
      let newFavorites = favorites.filter((f) => f.stop_id != stop.stop_id);
      newFavorites.push(stop);
      localStorage.setItem("favs", JSON.stringify(newFavorites));
      setFavorites(newFavorites);
    }
  }, [stop]);

  return favorites;
}
