import "tailwindcss/tailwind.css";

export async function Stock({ symbol, numOfMonths }: any) {
  //   const data = await fetch(
  //     `https://api.example.com/stock/${symbol}/${numOfMonths}`
  //   );
  console.log(symbol, numOfMonths);
  const data = {
    timeline: [
      { date: "2022-01-01", value: 100 },
      { date: "2022-02-01", value: 200 },
      { date: "2022-03-01", value: 300 },
      { date: "2022-04-01", value: 400 },
      { date: "2022-05-01", value: 500 },
      { date: "2022-06-01", value: 600 },
      { date: "2022-07-01", value: 700 },
      { date: "2022-08-01", value: 800 },
      { date: "2022-09-01", value: 900 },
      { date: "2022-10-01", value: 1000 },
      { date: "2022-11-01", value: 1100 },
      { date: "2022-12-01", value: 1200 },
    ],
  };

  return (
    <div className="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4">
        <div className="font-bold text-2xl mb-2 text-center">証券コード：{symbol}</div>
        <p className="text-gray-700 text-base text-center">
          過去{numOfMonths}ヶ月間のデータを表示
        </p>
      </div>
      <div className="px-6 py-4">
        {data.timeline.map((data, index) => (
          <div key={index} className="flex justify-between items-center border-b border-gray-200 py-2">
            <div className="text-gray-700">{data.date}</div>
            <div className="text-gray-900 font-semibold text-lg">{data.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
