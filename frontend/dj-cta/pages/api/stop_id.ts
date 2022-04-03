// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { NextApiRequest, NextApiResponse } from 'next'

const stop_id = async (req: NextApiRequest, res: NextApiResponse) => {
  const {
    query: { stpid }
  } = req;
  //console.log("This is running!");
  try {
    /*
    const data = await fetch(
      `https://dj-cta-2uyukedvua-uc.a.run.app/?stpid=${stpid}`
    );
    //console.log(data);
    const payload = await data.json();
    */
    // Dummy response
    const payload = {
      url: "",
      track_duration: 300,
      wait_duration: 120,
    }
    return res.status(200).json(payload);
  } catch(e) {
    return res.status(500).json(`${e}`)
  }
}

export default stop_id
