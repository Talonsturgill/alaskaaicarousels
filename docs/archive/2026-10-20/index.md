# Played Bethel's Yup'ik, the Model Answered Across the Sea

> Meta's model card says "This model supports 4017 languages." "Supports" for Yup'ik means one label in 4,017.

Published 2026-10-20 by Alaska AI. 9 slides.
Canonical: https://alaskaaihq.com/archive/2026-10-20/

## The story

Played Bethel's Yup'ik, the model most often answered across the sea.

111 to 110.

Played Yup'ik clips from KYUK's broadcasts, Meta's MMS-LID answered Central Siberian Yupik 111 times and Yup'ik 110. That language is spoken on St. Lawrence Island and in eastern Russia.

Three big open models list no Yupik at all.

Only Meta's largest model lists Yup'ik, one label in 4,017. The authors say a label space that big makes out-of-the-box results poor for languages with little data.

Central Siberian Yupik is a living language. One count puts about 1,000 speakers on St. Lawrence Island. The model's top miss was a near one.

The test audio came from Bethel's own station.

KYUK airs about an hour of local news in Yup'ik a day. The researchers labeled 9 of its videos, 5.1 hours, through the American Archive of Public Broadcasting.

The labeled hours lifted recall to 0.92.

Trained on labeled Yup'ik and Samoan clips, a small classifier on a frozen Whisper encoder lifted Yup'ik recall from 0.41 to 0.92. It chooses among four labels, not 4,017. The authors call it pilot-scale.

The next labels come from speakers.

The pilot's labels were written by in-house researchers, not native speakers. The authors plan to hand that work to trained native-speaker annotators, and community language fellows have begun, the paper says.

AFN is set to take up 26-20.

From the Metlakatla and Ketchikan Indian Communities, it seeks permanent, non-competitive federal language funding for every eligible Tribe. Technology and archives are among its uses. It never mentions AI. Committee and board say do pass.

Whoever labels the hours draws the map.

What does a model builder owe the speakers who write the next labels?

## What we verified

- A Brandeis University survey found no spoken language identification system on HuggingFace that covers Central Alaskan Yup'ik except the largest variant of Meta's MMS-LID family. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Whisper, VoxLingua107-based models and ESPnet OWSM include Hawaiian and Maori but neither Samoan nor any Yupik variety. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper's Table 1 lists Whisper large-v3 as covering 99 languages. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper's Table 1 lists VoxLingua107 as covering 107 languages. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper's Table 1 lists ESPnet OWSM v4 as covering about 150 languages. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Meta's MMS-LID family covers Yup'ik only at its largest variant, which has 4,017 labels. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- At 4,017 labels the per-class prior is about 2.5 x 10^-4, which the authors say makes zero-shot results on under-represented languages poor. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Zero-shot on the Yup'ik test clips, mms-lid-4017 reached a precision of 0.85 on the Yup'ik label. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Zero-shot on the Yup'ik test clips, mms-lid-4017 reached a recall of 0.41 on the Yup'ik label. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Zero-shot on the Yup'ik test clips, mms-lid-4017 reached an F1 score of 0.55 on the Yup'ik label. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- For gold Yup'ik clips, the most frequent label mms-lid-4017 predicted was ess, Central Siberian Yupik, with 111 clips. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- For gold Yup'ik clips, mms-lid-4017 predicted the correct label esu for 110 clips. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- For gold Yup'ik clips, mms-lid-4017 predicted esk, Northwest Alaska Inupiatun, for 16 clips. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- For gold Yup'ik clips, mms-lid-4017 predicted esi, North Alaskan Inupiatun, for 7 clips. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- ISO 639-3 code ess denotes Central Siberian Yupik, a living individual language. [SIL International, ISO 639-3 Registration Authority](https://iso639-3.sil.org/code/ess), primary document, 2026-10-21.
- ISO 639-3 code esk denotes Northwest Alaska Inupiatun, part of the Inupiaq macrolanguage. [SIL International, ISO 639-3 Registration Authority](https://iso639-3.sil.org/code/esk), primary document, 2026-10-21.
- ISO 639-3 code esi denotes North Alaskan Inupiatun, part of the Inupiaq macrolanguage. [SIL International, ISO 639-3 Registration Authority](https://iso639-3.sil.org/code/esi), primary document, 2026-10-21.
- The study's Yup'ik audio comes from KYUK, a public broadcaster in western Alaska that has produced Yup'ik television news and programming since the 1970s. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The researchers took their audio from the American Archive of Public Broadcasting Online Reading Room, a collaboration between GBH and the Library of Congress. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The annotated Yup'ik set covers 9 videos. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The annotated Yup'ik set runs 5.1 hours. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The annotated Yup'ik set contains 589 segments. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- 283 of the Yup'ik set's segments are labeled as Yup'ik speech, esu. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- A small classifier head trained on a frozen Whisper-medium encoder raised Yup'ik recall to 0.92. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- With the frozen Whisper-medium encoder the Yup'ik F1 score reached 0.94. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The same classifier head on a frozen XLS-R-300M encoder raised Yup'ik recall to 0.85. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- With the frozen XLS-R-300M encoder the Yup'ik F1 score reached 0.82. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The prototype is a two-layer MLP trained on fixed features from a frozen pretrained speech encoder. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The prototype was trained on about 1,600 labeled clips across both Yup'ik and Samoan, in four coarse classes. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The authors say their prototype results should be treated as pilot-scale evidence. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The authors' next step is to move primary annotation to trained native-speaker annotators. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Since the paper's first submission, community language fellows have begun annotating Yup'ik and Samoan broadcast material. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The current annotated set was labeled by in-house researchers rather than native speakers. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper describes Yup'ik as having a four-vowel system with contrastive vowel length. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper's Table 2 puts the Yup'ik consonant inventory at about 25. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper says Yup'ik has acoustically distinctive sounds rare across languages, including velar and uvular consonants and voiceless nasals. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- The paper by Yangyang Chen, Kyeongmin Rim and James Pustejovsky of Brandeis University appeared in the AmericasNLP 2026 workshop proceedings on July 3rd. [ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18/), primary document, 2026-07-03.
- The research was supported in part by the Andrew W. Mellon Foundation. [Chen, Rim and Pustejovsky (Brandeis University), AmericasNLP 2026 proceedings, ACL Anthology](https://aclanthology.org/2026.americasnlp-6.18.pdf), primary document, 2026-07-03.
- Meta's Massively Multilingual Speech paper describes a language identification model for 4,017 languages. [Pratap et al. (Meta AI), arXiv](https://arxiv.org/abs/2305.13516), primary document, 2023-05-22.
- Meta's mms-lid-4017 model card on HuggingFace says the model supports 4017 languages. [Meta (facebook) on HuggingFace](https://huggingface.co/facebook/mms-lid-4017), primary document, 2026-10-21.
- KYUK's licensee operates public radio and television stations in Bethel, Alaska. [KYUK (Bethel Broadcasting, Inc.)](https://www.kyuk.org/history-and-mission), primary document, 2026-10-21.
- KYUK radio has been on the air since 1971. [KYUK (Bethel Broadcasting, Inc.)](https://www.kyuk.org/history-and-mission), primary document, 2026-10-21.
- KYUK television began broadcasting in 1972. [KYUK (Bethel Broadcasting, Inc.)](https://www.kyuk.org/history-and-mission), primary document, 2026-10-21.
- KYUK broadcasts about one hour a day of local news in Yup'ik. [KYUK (Bethel Broadcasting, Inc.)](https://www.kyuk.org/history-and-mission), primary document, 2026-10-21.
- KYUK describes itself as a bilingual station broadcasting in English and Yugtun. [American Archive of Public Broadcasting, KYUK participating-organization profile](https://americanarchive.org/participating-orgs/1703), primary document, 2026-10-21.
- KYUK radio serves about 22,000 mostly Yup'ik and Cup'ik residents of the Yukon-Kuskokwim Delta. [American Archive of Public Broadcasting, KYUK participating-organization profile](https://americanarchive.org/participating-orgs/1703), primary document, 2026-10-21.
- KYUK says it is digitizing more than 2,000 videos to make them public. [American Archive of Public Broadcasting, KYUK participating-organization profile](https://americanarchive.org/participating-orgs/1703), primary document, 2026-10-21.
- AFN draft resolution 26-20 is titled a resolution supporting national Indigenous language revitalization, Tribal self-governance and permanent federal funding. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-20 calls on Congress and the Administration to establish permanent, non-competitive federal funding for all eligible Tribal Nations to revitalize their languages. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-20 lists technology among the uses Tribes could fund, alongside immersion schools, master-apprentice programs, curriculum, archives and community-based transmission. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-20 states that competitive, short-term grant funding has proven inadequate and inconsistent with Tribal self-determination. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- The full text of resolution 26-20 names technology as a fundable use but never mentions artificial intelligence. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-20 was submitted by the Metlakatla Indian Community and the Ketchikan Indian Community. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's resolutions committee recommended do pass on resolution 26-20. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's board recommended do pass on resolution 26-20. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- In the September 27th draft packet the convention action line for resolution 26-20 is blank, so delegates had not yet voted. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's resolutions state that its membership includes 192 federally recognized tribes. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's resolutions state that its membership includes 152 village corporations. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's resolutions state that its membership includes 11 regional corporations. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- AFN's resolutions state that its membership includes 11 regional nonprofit and tribal consortiums. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- The 2026 AFN Annual Convention runs October 22nd through October 24th. [Alaska Federation of Natives](https://nativefederation.org/convention/), primary document, 2026-10-21.
- The 2026 AFN Annual Convention is in Anchorage. [Alaska Federation of Natives](https://nativefederation.org/convention/), primary document, 2026-10-21.
- AFN delegates take up the 2026 convention resolutions on Saturday, October 24th, in a session starting at a quarter past ten in the morning. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/10/2026-Annual-Convention-Agenda_10.16.26.pdf), primary document, 2026-10-16.
- The resolutions session is moderated by Jodi Mitchell, chair of AFN's Resolutions Committee. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/10/2026-Annual-Convention-Agenda_10.16.26.pdf), primary document, 2026-10-16.
- AFN's 2026 draft resolution packet contains 48 resolutions. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- None of the 48 resolution titles in AFN's 2026 draft packet names artificial intelligence, AI or data centers. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-21 asks the University of Alaska system to create academic credit and credential pathways for tribal training programs. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-21 was submitted by Tanana Chiefs Conference. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-47 urges Congress to appropriate 14.9 million dollars a year to the Bureau of Indian Affairs to sustain 36 Native radio stations and one Tribally licensed television station. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-47 was submitted by Cook Inlet Region, Inc. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Resolution 26-47 states that Alaska public media lost annual state funding in August 2019 and annual Corporation for Public Broadcasting funding in October 2025. [Alaska Federation of Natives](https://nativefederation.org/wp-content/uploads/2026/09/AFN-2026-Resolutions-9.27.26-final.pdf), primary document, 2026-09-27.
- Yup'ik has the largest body of speakers of any Alaska Native language, according to the Alaska Native Languages site. [Alaska Native Languages (alaskanativelanguages.org), maps credited to the Alaska Native Language Center](https://www.alaskanativelanguages.org/yugtun-yup-ik), report, 2026-10-21.
- The Alaska Native Languages site puts the number of native Yup'ik speakers at 10,400. [Alaska Native Languages (alaskanativelanguages.org)](https://www.alaskanativelanguages.org/yugtun-yup-ik), report, 2026-10-21.
- Central Alaskan Yup'ik is spoken in Southwest Alaska from Bristol Bay to Norton Sound. [Alaska Native Languages (alaskanativelanguages.org)](https://www.alaskanativelanguages.org/yugtun-yup-ik), report, 2026-10-21.
- St. Lawrence Island Yupik is spoken by about 1,000 people on St. Lawrence Island, according to the Alaska Native Languages site. [Alaska Native Languages (alaskanativelanguages.org)](https://www.alaskanativelanguages.org/yupigestun-sli-yupik), report, 2026-10-21.
- The same Yupik language is also spoken in eastern Russia. [Alaska Native Languages (alaskanativelanguages.org)](https://www.alaskanativelanguages.org/yupigestun-sli-yupik), report, 2026-10-21.
- Glottolog lists St. Lawrence Island Yupik as an alternative name for Central Siberian Yupik and records it in Russia and the United States. [Glottolog (Max Planck Institute for Evolutionary Anthropology)](https://glottolog.org/resource/languoid/iso/ess), report, 2026-10-21.
- The convention is being held at Anchorage's Dena'ina Civic and Convention Center. [Alaska Public Media (Alena Naiden, KNBA, Alaska Desk)](https://alaskapublic.org/news/alaska-desk/2026-10-19/alaska-federation-of-natives-convention-celebrates-60th-anniversary-this-week), report, 2026-10-19.
- This year's AFN convention marks the organization's 60th anniversary. [Alaska Public Media (Alena Naiden, KNBA, Alaska Desk)](https://alaskapublic.org/news/alaska-desk/2026-10-19/alaska-federation-of-natives-convention-celebrates-60th-anniversary-this-week), report, 2026-10-19.

Slides and the deck PDF are linked from the canonical page.
