from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
import streamlit

RATES = {
    "AED": 3.673,
    "AFN": 73,
    "ALL": 96.25,
    "AMD": 405.903361,
    "ANG": 1.803035,
    "AOA": 831.5,
    "ARS": 835.05,
    "AUD": 1.531309,
    "AWG": 1.8,
    "AZN": 1.7,
    "BAM": 1.815203,
    "BBD": 2,
    "BDT": 109.785984,
    "BGN": 1.814895,
    "BHD": 0.376896,
    "BIF": 2866,
    "BMD": 1,
    "BND": 1.346321,
    "BOB": 6.91326,
    "BRL": 4.9671,
    "BSD": 1,
    "BTC": 0.000019339251,
    "BTN": 83.038296,
    "BWP": 13.694307,
    "BYN": 3.273733,
    "BZD": 2.016418,
    "CAD": 1.348891,
    "CDF": 2755,
    "CHF": 0.880733,
    "CLF": 0.035176,
    "CLP": 971.4,
    "CNH": 7.21277,
    "CNY": 7.1193,
    "COP": 3909.472351,
    "CRC": 516.638232,
    "CUC": 1,
    "CUP": 25.75,
    "CVE": 102.85,
    "CZK": 23.60815,
    "DJF": 177.827972,
    "DKK": 6.917185,
    "DOP": 58.6,
    "DZD": 134.579251,
    "EGP": 30.9039,
    "ERN": 15,
    "ETB": 56.63,
    "EUR": 0.92791,
    "FJD": 2.2442,
    "FKP": 0.793525,
    "GBP": 0.793525,
    "GEL": 2.64375,
    "GGP": 0.793525,
    "GHS": 12.47,
    "GIP": 0.793525,
    "GMD": 67.75,
    "GNF": 8605,
    "GTQ": 7.81176,
    "GYD": 209.309977,
    "HKD": 7.82215,
    "HNL": 24.68862,
    "HRK": 6.99138,
    "HTG": 131.931261,
    "HUF": 361.0155,
    "IDR": 15655.6,
    "ILS": 3.606,
    "IMP": 0.793525,
    "INR": 83.0143,
    "IQD": 1310,
    "IRR": 42030,
    "ISK": 138,
    "JEP": 0.793525,
    "JMD": 156.563407,
    "JOD": 0.7091,
    "JPY": 150.22503727,
    "KES": 145,
    "KGS": 89.43,
    "KHR": 4081.5,
    "KMF": 457.450353,
    "KPW": 900,
    "KRW": 1332.58,
    "KWD": 0.307979,
    "KYD": 0.833631,
    "KZT": 450.039931,
    "LAK": 20870,
    "LBP": 15030,
    "LKR": 312.596283,
    "LRD": 190.500063,
    "LSL": 18.88,
    "LYD": 4.855,
    "MAD": 10.063,
    "MDL": 17.830168,
    "MGA": 4537.5,
    "MKD": 57.22817,
    "MMK": 2100.688499,
    "MNT": 3450,
    "MOP": 8.06024,
    "MRU": 39.59,
    "MUR": 46.829999,
    "MVR": 15.4,
    "MWK": 1682,
    "MXN": 17.0526,
    "MYR": 4.78,
    "MZN": 63.899991,
    "NAD": 18.88,
    "NGN": 1493.73,
    "NIO": 36.75,
    "NOK": 10.448405,
    "NPR": 132.861181,
    "NZD": 1.631854,
    "OMR": 0.384952,
    "PAB": 1,
    "PEN": 3.869,
    "PGK": 3.73925,
    "PHP": 55.97,
    "PKR": 279.5,
    "PLN": 4.026766,
    "PYG": 7295.675193,
    "QAR": 3.641,
    "RON": 4.6184,
    "RSD": 108.732,
    "RUB": 91.99632,
    "RWF": 1272.5,
    "SAR": 3.750196,
    "SBD": 8.432716,
    "SCR": 13.552857,
    "SDG": 601,
    "SEK": 10.45981,
    "SGD": 1.34996,
    "SHP": 0.793525,
    "SLL": 20969.5,
    "SOS": 571.5,
    "SRD": 36.3345,
    "SSP": 130.26,
    "STD": 22281.8,
    "STN": 23.15,
    "SVC": 8.752993,
    "SYP": 2512.53,
    "SZL": 18.88,
    "THB": 35.922106,
    "TJS": 10.949738,
    "TMT": 3.5,
    "TND": 3.1385,
    "TOP": 2.369021,
    "TRY": 30.8424,
    "TTD": 6.787952,
    "TWD": 31.3482,
    "TZS": 2545,
    "UAH": 38.079548,
    "UGX": 3874.848573,
    "USD": 1,
    "UYU": 39.114845,
    "UZS": 12505,
    "VES": 36.228384,
    "VND": 24530.865624,
    "VUV": 118.722,
    "WST": 2.8,
    "XAF": 608.669375,
    "XAG": 0.04270493,
    "XAU": 0.00049677,
    "XCD": 2.70255,
    "XDR": 0.754927,
    "XOF": 608.669375,
    "XPD": 0.00105364,
    "XPF": 110.729174,
    "XPT": 0.00110108,
    "YER": 250.374948,
    "ZAR": 18.90581,
    "ZMW": 26.253158,
    "ZWL": 322
}


def fetch_rate(target):
    return RATES.get(target, 0)


@tool
def currency_converter(source: str, target: str, amount: float):
    """
    if user asks currency exchange rate related questions, you should call this function. But if the source currency is other than USD (US Dollar), you should ignore calling tools.
    - source: The source currency to be queried in 3-letter ISO 4217 format.
    - target: The target currency to be queried in 3-letter ISO 4217 format.
    - amount: The amount of the currency to be converted to the target currency.
    """
    rate = fetch_rate(target)
    total = rate * amount
    return f"based on today's exchange rate: {rate}, {amount} {source} is equivalent to approximately {total} {target}"


def main():
    llm = ChatOpenAI(model_name="gpt-4o").bind_tools([currency_converter])

    system_prompt = "You are a very helpful assistant. Your job is to choose the best possible action to solve the user question or task. Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."

    streamlit.title("Currency converter")
    user_question = streamlit.text_input("Ask a question about currency:")

    if user_question:
        messages = [SystemMessage(system_prompt), HumanMessage(user_question)]
        ai_msg = llm.invoke(messages)
        messages.append(ai_msg)
        for tc in ai_msg.tool_calls:
            if tc["name"] == "currency_converter":
                output = currency_converter.invoke(tc["args"])
                messages.append(ToolMessage(output, tool_call_id=tc["id"]))
                response = llm.invoke(messages).content
                streamlit.write(response)


if __name__ == "__main__":
    main()
