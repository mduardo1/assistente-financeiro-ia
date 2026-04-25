import re
import unicodedata
from datetime import date


class ParserService:
    EXPENSE_KEYWORDS = {"gastei", "paguei", "comprei", "saiu", "despesa"}
    INCOME_KEYWORDS = {"recebi", "ganhei", "vendi", "entrou", "receita"}

    def parse_message(self, message: str) -> dict[str, str]:
        normalized_message = message.strip()

        if not normalized_message:
            raise ValueError("Envie uma mensagem para interpretar.")

        cleaned_message = self._normalize(normalized_message)
        keyword = cleaned_message.split()[0]

        if keyword in self.EXPENSE_KEYWORDS:
            transaction_type = "expense"
        elif keyword in self.INCOME_KEYWORDS:
            transaction_type = "income"
        else:
            raise ValueError("Não consegui identificar se a mensagem é entrada ou saída.")

        amount_match = re.search(r"(\d+(?:[.,]\d{1,2})?)", cleaned_message)
        if amount_match is None:
            raise ValueError("Não encontrei um valor financeiro na mensagem.")

        amount = amount_match.group(1).replace(",", ".")
        category = self._extract_category(cleaned_message, keyword, amount_match.group(0))

        return {
            "type": transaction_type,
            "description": normalized_message,
            "category": category,
            "amount": amount,
            "transaction_date": date.today().isoformat(),
        }

    def _extract_category(self, message: str, keyword: str, amount: str) -> str:
        patterns = [
            rf"{keyword}\s+{amount}\s+no\s+(.+)$",
            rf"{keyword}\s+{amount}\s+na\s+(.+)$",
            rf"{keyword}\s+{amount}\s+de\s+(.+)$",
            rf"{keyword}\s+{amount}\s+do\s+(.+)$",
            rf"{keyword}\s+{amount}\s+da\s+(.+)$",
            rf"{keyword}\s+{amount}\s+em\s+(.+)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, message)
            if match is not None:
                return match.group(1).strip()

        remaining = re.sub(rf"^{keyword}\s+{amount}\s*", "", message).strip()
        return remaining or "geral"

    def _normalize(self, value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.lower())
        return "".join(character for character in normalized if not unicodedata.combining(character))
